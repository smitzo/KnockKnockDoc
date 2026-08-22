import secrets
from dataclasses import dataclass
from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from apps.identity.models import (
    IdentityStatus,
    MembershipRole,
    MembershipStatus,
    OrganizationMembership,
    OrganizationStatus,
    SecurityAction,
)
from apps.identity.services import record_security_event

from .models import (
    AccessScope,
    AssignmentStatus,
    CaseAccessGrant,
    CaseAssignment,
    CaseEvent,
    CaseParticipant,
    CaseStatus,
    ConsentStatus,
    GrantScope,
    ParticipantRole,
    ReferralCase,
)


@dataclass(frozen=True)
class CreateReferralCommand:
    patient_alias: str
    patient_country: str
    patient_age_band: str
    specialty: str
    clinical_question: str
    summary: str


def _new_reference() -> str:
    return f"KND-{timezone.now():%y%m}-{secrets.token_hex(3).upper()}"


def _lock_active_referrer_membership(
    membership: OrganizationMembership,
) -> OrganizationMembership:
    now = timezone.now()
    try:
        return (
            OrganizationMembership.objects.select_for_update()
            .select_related("organization", "user__identity_profile")
            .get(
                Q(id=membership.id)
                & Q(user=membership.user)
                & Q(user__is_active=True)
                & Q(role=MembershipRole.REFERRER)
                & Q(status=MembershipStatus.ACTIVE)
                & Q(starts_at__lte=now)
                & (Q(ends_at__isnull=True) | Q(ends_at__gt=now))
                & Q(organization__status=OrganizationStatus.ACTIVE)
                & Q(user__identity_profile__status=IdentityStatus.ACTIVE)
                & Q(user__identity_profile__email_verified_at__isnull=False)
            )
        )
    except OrganizationMembership.DoesNotExist as exc:
        raise PermissionDenied("An active verified referrer membership is required.") from exc


@transaction.atomic
def create_referral_case(
    command: CreateReferralCommand,
    *,
    referrer_membership: OrganizationMembership,
) -> ReferralCase:
    referrer_membership = _lock_active_referrer_membership(referrer_membership)
    referrer_profile = referrer_membership.user.identity_profile
    reference = _new_reference()
    while ReferralCase.objects.filter(reference=reference).exists():
        reference = _new_reference()

    referral = ReferralCase.objects.create(
        reference=reference,
        patient_alias=command.patient_alias,
        patient_country=command.patient_country,
        patient_age_band=command.patient_age_band,
        specialty=command.specialty,
        clinical_question=command.clinical_question,
        summary=command.summary,
        status=CaseStatus.AWAITING_CONSENT,
        consent_status=ConsentStatus.PENDING,
        is_planned_care=True,
        is_synthetic=True,
        corridor_label=f"{command.patient_country} → India · {command.specialty}",
        next_action="Review the referral purpose and synthetic sharing preview.",
        next_action_owner=command.patient_alias,
        next_action_due=timezone.now() + timedelta(days=2),
    )
    CaseParticipant.objects.bulk_create(
        [
            CaseParticipant(
                case=referral,
                display_name=command.patient_alias,
                role=ParticipantRole.PATIENT,
                access_scope="Synthetic case summary and activity",
                access_state="active",
                purpose="Review the prototype referral",
            ),
            CaseParticipant(
                case=referral,
                display_name=referrer_profile.display_name,
                role=ParticipantRole.REFERRER,
                organization=referrer_membership.organization.name,
                access_scope="Referral summary and synthetic record metadata",
                access_state="active",
                purpose="Create and coordinate the referral rehearsal",
            ),
        ]
    )
    assignment = CaseAssignment.objects.create(
        case=referral,
        membership=referrer_membership,
        purpose="Create and coordinate this synthetic referral rehearsal",
        status=AssignmentStatus.ACTIVE,
    )
    grant = CaseAccessGrant.objects.create(
        assignment=assignment,
        purpose="Coordinate the synthetic referral created by this referrer",
        granted_by=referrer_membership.user,
        expires_at=timezone.now() + timedelta(days=90),
    )
    GrantScope.objects.bulk_create(
        [
            GrantScope(grant=grant, scope=AccessScope.CASE_VIEW),
            GrantScope(grant=grant, scope=AccessScope.CASE_EDIT),
            GrantScope(grant=grant, scope=AccessScope.CASE_MANAGE),
        ]
    )
    CaseEvent.objects.create(
        case=referral,
        event_type="referral_created",
        actor_label=referrer_profile.display_name,
        actor_role="Referring doctor",
        summary="Created a synthetic referral rehearsal; patient review is next.",
        occurred_at=timezone.now(),
    )
    record_security_event(
        action=SecurityAction.CASE_CREATED,
        actor=referrer_membership.user,
        organization=referrer_membership.organization,
        target_type="referral_case",
        target_id=referral.id,
        metadata={"membership_role": referrer_membership.role},
    )

    from .tasks import record_case_created

    transaction.on_commit(lambda: record_case_created.delay(str(referral.id)))
    return referral
