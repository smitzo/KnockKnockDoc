from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError, transaction

from apps.identity.models import SecurityAction
from apps.identity.services import normalize_login_email, record_security_event

from .models import (
    ApplicationType,
    DoctorApplicationDetails,
    HospitalApplicationDetails,
    PartnerApplication,
)


@dataclass(frozen=True)
class ApplicationSubmissionResult:
    created: bool


class ApplicationPasswordError(ValueError):
    pass


@transaction.atomic
def submit_partner_application(*, validated_data: dict) -> ApplicationSubmissionResult:
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
