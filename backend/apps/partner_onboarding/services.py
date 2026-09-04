from dataclasses import dataclass

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.utils.text import slugify

from apps.demo_lab.selectors import lock_demo_mode_enabled
from apps.identity.models import (
    AccountType,
    IdentityProfile,
    IdentityStatus,
    MembershipRole,
    MembershipStatus,
    Organization,
    OrganizationMembership,
    OrganizationStatus,
    OrganizationType,
    SecurityAction,
    VerificationBasis,
)
from apps.identity.selectors import active_memberships_for_user
from apps.identity.services import normalize_login_email, record_security_event
from apps.professional_network.models import (
    ProfessionalDirectoryProfile,
    VerificationState,
)

from .models import (
    ApplicationStatus,
    ApplicationType,
    DoctorApplicationDetails,
    HospitalApplicationDetails,
    PartnerApplication,
    ReviewReason,
)


@dataclass(frozen=True)
class ApplicationSubmissionResult:
    created: bool


class ApplicationPasswordError(ValueError):
    pass


class ApplicationDemoModeError(ValueError):
    pass


class ApplicationReviewError(ValueError):
    pass


REVIEW_TRANSITIONS = {
    "start_review": {
        "from": {ApplicationStatus.SUBMITTED, ApplicationStatus.CHANGES_REQUESTED},
        "to": ApplicationStatus.UNDER_REVIEW,
        "action": SecurityAction.ONBOARDING_REVIEW_STARTED,
    },
    "request_changes": {
        "from": {ApplicationStatus.UNDER_REVIEW},
        "to": ApplicationStatus.CHANGES_REQUESTED,
        "action": SecurityAction.ONBOARDING_CHANGES_REQUESTED,
    },
    "approve": {
        "from": {ApplicationStatus.UNDER_REVIEW},
        "to": ApplicationStatus.APPROVED,
        "action": SecurityAction.ONBOARDING_APPLICATION_APPROVED,
    },
    "reject": {
        "from": {ApplicationStatus.UNDER_REVIEW},
        "to": ApplicationStatus.REJECTED,
        "action": SecurityAction.ONBOARDING_APPLICATION_REJECTED,
    },
}


@transaction.atomic
def submit_partner_application(*, validated_data: dict) -> ApplicationSubmissionResult:
    if not lock_demo_mode_enabled():
        raise ApplicationDemoModeError("Demo data is not enabled.")
    password = validated_data.pop("password")
    details = validated_data.pop("details")
    email = normalize_login_email(validated_data.pop("email"))
    user_model = get_user_model()
    validation_user = user_model(username=email, email=email, is_active=False)
    try:
        validate_password(password, user=validation_user)
    except DjangoValidationError as exc:
        raise ApplicationPasswordError("Choose a stronger passphrase.") from exc

    if user_model.objects.filter(username=email).exists():
        return ApplicationSubmissionResult(created=False)

    try:
        with transaction.atomic():
            user = user_model.objects.create_user(
                username=email,
                email=email,
                password=password,
                is_active=False,
            )
            application = PartnerApplication.objects.create(
                user=user,
                normalized_email=email,
                **validated_data,
            )
            if application.application_type == ApplicationType.DOCTOR:
                DoctorApplicationDetails.objects.create(application=application, **details)
            else:
                HospitalApplicationDetails.objects.create(application=application, **details)
    except IntegrityError:
        return ApplicationSubmissionResult(created=False)

    record_security_event(
        action=SecurityAction.ONBOARDING_APPLICATION_SUBMITTED,
        actor=user,
        target_type="partner_application",
        target_id=application.id,
        metadata={"application_type": application.application_type},
    )
    return ApplicationSubmissionResult(created=True)


@transaction.atomic
def review_partner_application(
    *,
    actor,
    application_id,
    action: str,
    reason_code: str = "",
    reviewer_note: str = "",
) -> PartnerApplication:
    transition = REVIEW_TRANSITIONS.get(action)
    if transition is None:
        raise ApplicationReviewError("Unknown review action.")
    admin_membership = (
        active_memberships_for_user(actor)
        .filter(
            role=MembershipRole.ADMIN,
            organization__organization_type=OrganizationType.PLATFORM,
        )
        .first()
    )
    if admin_membership is None:
        raise ApplicationReviewError("A platform administrator is required.")
    if not lock_demo_mode_enabled():
        raise ApplicationReviewError("Demo data is not enabled.")

    application = (
        PartnerApplication.objects.select_for_update()
        .select_related("user", "doctor_details", "hospital_details")
        .filter(id=application_id)
        .first()
    )
    if application is None:
        raise ApplicationReviewError("Application not found.")
    if application.status not in transition["from"]:
        raise ApplicationReviewError(
            f"Application cannot move from {application.status} using {action}."
        )
    if action in {"request_changes", "reject"} and reason_code not in ReviewReason.values:
        raise ApplicationReviewError("A valid reason code is required.")

    now = timezone.now()
    activated_organization = None
    if action == "approve":
        activated_organization = _activate_synthetic_application(application, now=now)

    application.status = transition["to"]
    application.reviewer = actor
    application.reviewed_at = now
    application.review_reason_code = (
        reason_code if action in {"request_changes", "reject"} else ""
    )
    application.reviewer_note = reviewer_note
    if action == "approve":
        application.activated_at = now
        application.activated_organization = activated_organization
    application.save(
        update_fields=[
            "status",
            "reviewer",
            "reviewed_at",
            "review_reason_code",
            "reviewer_note",
            "activated_at",
            "activated_organization",
            "updated_at",
        ]
    )
    metadata = {
        "application_type": application.application_type,
        "transition_result": application.status,
    }
    if application.review_reason_code:
        metadata["reason_code"] = application.review_reason_code
    record_security_event(
        action=transition["action"],
        actor=actor,
        organization=admin_membership.organization,
        target_type="partner_application",
        target_id=application.id,
        metadata=metadata,
    )
    return application


def _activate_synthetic_application(application: PartnerApplication, *, now) -> Organization:
    if not settings.PROTOTYPE_MODE or not application.is_synthetic:
        raise ApplicationReviewError("Only synthetic prototype applications can be activated.")
    if not application.normalized_email.lower().endswith(".test"):
        raise ApplicationReviewError("Synthetic activation requires a .test account.")
    if (
        IdentityProfile.objects.filter(user=application.user).exists()
        or OrganizationMembership.objects.filter(user=application.user).exists()
        or ProfessionalDirectoryProfile.objects.filter(user=application.user).exists()
    ):
        raise ApplicationReviewError("The application already has an access projection.")

    organization_type = OrganizationType.HOSPITAL
    account_type = AccountType.COORDINATOR
    membership_role = MembershipRole.HOSPITAL_COORDINATOR
    if application.application_type == ApplicationType.DOCTOR:
        details = application.doctor_details
        account_type = AccountType.PROFESSIONAL
        membership_role = details.professional_role
        organization_type = (
            OrganizationType.REFERRING_PRACTICE
            if details.professional_role == MembershipRole.REFERRER
            else OrganizationType.HOSPITAL
        )

    slug_root = slugify(application.organization_name)[:58] or "partner"
    organization = Organization.objects.create(
        name=application.organization_name,
        slug=f"{slug_root}-{str(application.id)[:8]}",
        organization_type=organization_type,
        status=OrganizationStatus.ACTIVE,
    )
    IdentityProfile.objects.create(
        user=application.user,
        normalized_email=application.normalized_email,
        display_name=application.display_name,
        account_type=account_type,
        status=IdentityStatus.ACTIVE,
        email_verified_at=now,
        verification_basis=VerificationBasis.SYNTHETIC_ADMIN_REVIEW,
    )
    OrganizationMembership.objects.create(
        user=application.user,
        organization=organization,
        role=membership_role,
        status=MembershipStatus.ACTIVE,
        starts_at=now,
    )
    if application.application_type == ApplicationType.DOCTOR:
        details = application.doctor_details
        ProfessionalDirectoryProfile.objects.create(
            user=application.user,
            professional_role=details.professional_role,
            specialty=details.primary_specialty,
            experience_years=max(0, now.year - details.experience_start_year),
            country=application.country,
            city=application.city,
            organization_name=application.organization_name,
            languages=details.languages,
            professional_summary=application.professional_summary,
            avatar_key=f"review-{str(application.id).replace('-', '')[:16]}",
            verification_state=VerificationState.SYNTHETIC_ADMIN_REVIEW,
            is_discoverable=True,
            accepts_connections=True,
            is_synthetic=True,
        )
    application.user.is_active = True
    application.user.save(update_fields=["is_active"])
    return organization
