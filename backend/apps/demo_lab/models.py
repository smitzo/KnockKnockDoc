from django.conf import settings
from django.db import models
from django.db.models import Q

from apps.core.models import UUIDTimeStampedModel


class DoctorAvailability(models.TextChoices):
    ACCEPTING = "accepting", "Accepting synthetic reviews"
    LIMITED = "limited", "Limited synthetic capacity"
    PAUSED = "paused", "Paused"


class SyntheticDoctorProfile(UUIDTimeStampedModel):
    fixture_key = models.CharField(max_length=40, unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="synthetic_doctor_profile",
        on_delete=models.PROTECT,
    )
    display_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    hospital_name = models.CharField(max_length=140)
    experience_years = models.PositiveSmallIntegerField()
    languages = models.JSONField(default=list)
    availability = models.CharField(max_length=20, choices=DoctorAvailability.choices)
    response_hours = models.PositiveSmallIntegerField()
    credential_state = models.CharField(max_length=32, default="synthetic_verified")
    avatar_key = models.CharField(max_length=40)
    profile_summary = models.CharField(max_length=280)
    is_synthetic = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_name"]
        constraints = [
            models.CheckConstraint(condition=Q(is_synthetic=True), name="demo_doctor_synthetic")
        ]
        indexes = [
            models.Index(fields=["specialty", "city"], name="demo_doctor_search_idx"),
            models.Index(fields=["availability"], name="demo_doctor_avail_idx"),
        ]


class PatientJourneyStage(models.TextChoices):
    INTAKE = "intake", "Intake"
    CONSENT = "consent", "Sharing review"
    COMPLETENESS = "completeness", "Completeness review"
    PROVIDER_REVIEW = "provider_review", "Provider review"
    RESPONSE = "response", "Response received"
    DECISION = "decision", "Patient decision"
    HANDBACK = "handback", "Home-doctor handback"


class SyntheticPatientProfile(UUIDTimeStampedModel):
    fixture_key = models.CharField(max_length=40, unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="synthetic_patient_profile",
        on_delete=models.PROTECT,
    )
    display_alias = models.CharField(max_length=100)
    home_country = models.CharField(max_length=80)
    age_band = models.CharField(max_length=20)
    specialty_interest = models.CharField(max_length=80)
    journey_stage = models.CharField(max_length=24, choices=PatientJourneyStage.choices)
    preferred_city = models.CharField(max_length=80)
    language = models.CharField(max_length=60)
    coordination_need = models.CharField(max_length=180)
    avatar_key = models.CharField(max_length=40)
    is_synthetic = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_alias"]
        constraints = [
            models.CheckConstraint(condition=Q(is_synthetic=True), name="demo_patient_synthetic")
        ]
        indexes = [
            models.Index(
                fields=["journey_stage", "specialty_interest"],
                name="demo_patient_flow_idx",
            ),
            models.Index(fields=["home_country"], name="demo_patient_country_idx"),
        ]
