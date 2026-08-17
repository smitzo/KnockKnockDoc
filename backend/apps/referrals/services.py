import secrets
from dataclasses import dataclass
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .models import (
    CaseEvent,
    CaseParticipant,
    CaseStatus,
    ConsentStatus,
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
    referrer_display_name: str
    referrer_country: str


def _new_reference() -> str:
    return f"KND-{timezone.now():%y%m}-{secrets.token_hex(3).upper()}"


@transaction.atomic
def create_referral_case(command: CreateReferralCommand) -> ReferralCase:
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
        corridor_label=f"{command.referrer_country} → India · {command.specialty}",
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
                display_name=command.referrer_display_name,
                role=ParticipantRole.REFERRER,
                organization=f"Synthetic referrer · {command.referrer_country}",
                access_scope="Referral summary and synthetic record metadata",
                access_state="active",
                purpose="Create and coordinate the referral rehearsal",
            ),
        ]
    )
    CaseEvent.objects.create(
        case=referral,
        event_type="referral_created",
        actor_label=command.referrer_display_name,
        actor_role="Referring doctor",
        summary="Created a synthetic referral rehearsal; patient review is next.",
        occurred_at=timezone.now(),
    )

    from .tasks import record_case_created

    transaction.on_commit(lambda: record_case_created.delay(str(referral.id)))
    return referral
