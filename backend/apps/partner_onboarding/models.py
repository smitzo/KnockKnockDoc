from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone as django_timezone

from apps.core.models import UUIDTimeStampedModel


class ApplicationType(models.TextChoices):
    DOCTOR = "doctor", "Doctor"
    HOSPITAL = "hospital", "Hospital"


class ApplicationStatus(models.TextChoices):
    SUBMITTED = "submitted", "Submitted"
    UNDER_REVIEW = "under_review", "Under review"
    CHANGES_REQUESTED = "changes_requested", "Changes requested"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"
    WITHDRAWN = "withdrawn", "Withdrawn"


class PartnerApplication(UUIDTimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="partner_application",
        on_delete=models.PROTECT,
    )
    normalized_email = models.EmailField(max_length=254, unique=True)
    application_type = models.CharField(max_length=16, choices=ApplicationType.choices)
    status = models.CharField(
        max_length=24,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.SUBMITTED,
    )
    legal_name = models.CharField(max_length=120)
    display_name = models.CharField(max_length=120)
    country = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    timezone = models.CharField(max_length=64)
    preferred_language = models.CharField(max_length=40)
    organization_name = models.CharField(max_length=140)
    professional_summary = models.CharField(max_length=500)
    terms_version = models.CharField(max_length=40)
    terms_accepted_at = models.DateTimeField(default=django_timezone.now, editable=False)
    is_synthetic = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=Q(is_synthetic=True),
                name="onboarding_application_synthetic",
            )
        ]
        indexes = [
            models.Index(
                fields=["application_type", "status", "-created_at"],
                name="onboarding_type_status_idx",
            )
        ]


class DoctorApplicationDetails(UUIDTimeStampedModel):
    application = models.OneToOneField(
        PartnerApplication,
        related_name="doctor_details",
        on_delete=models.CASCADE,
    )
    professional_role = models.CharField(max_length=24)
    primary_specialty = models.CharField(max_length=80)
    subspecialties = models.JSONField(default=list)
    current_designation = models.CharField(max_length=100)
    experience_start_year = models.PositiveSmallIntegerField()
    council_jurisdiction = models.CharField(max_length=100)
    synthetic_registration_number = models.CharField(max_length=80)
    qualifications = models.JSONField(default=list)
    languages = models.JSONField(default=list)


class HospitalApplicationDetails(UUIDTimeStampedModel):
    application = models.OneToOneField(
        PartnerApplication,
        related_name="hospital_details",
        on_delete=models.CASCADE,
    )
    organization_type = models.CharField(max_length=40)
    representative_title = models.CharField(max_length=100)
    website_url = models.URLField(max_length=240)
    establishment_year = models.PositiveSmallIntegerField()
    departments = models.JSONField(default=list)
    accreditation_labels = models.JSONField(default=list)
    bed_count = models.PositiveIntegerField()
    capacity_as_of = models.DateField()
    international_patient_services = models.JSONField(default=list)
    languages = models.JSONField(default=list)
