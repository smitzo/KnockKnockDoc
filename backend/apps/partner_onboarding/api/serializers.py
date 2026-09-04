import re
from datetime import date
from urllib.parse import urlparse

from rest_framework import serializers

from ..models import ApplicationStatus, ApplicationType, PartnerApplication, ReviewReason


TERMS_VERSION = "prototype-2026-08-11"
SYNTHETIC_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.test$", re.IGNORECASE)
SYNTHETIC_REGISTRATION_PATTERN = re.compile(r"^SYN-[A-Z0-9-]{4,40}$")


class PartnerApplicationSerializer(serializers.Serializer):
    application_type = serializers.ChoiceField(choices=ApplicationType.choices)
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(
        min_length=14,
        max_length=256,
        trim_whitespace=False,
        write_only=True,
    )
    legal_name = serializers.CharField(min_length=2, max_length=120)
    display_name = serializers.CharField(min_length=2, max_length=120)
    country = serializers.CharField(min_length=2, max_length=80)
    city = serializers.CharField(min_length=2, max_length=80)
    timezone = serializers.CharField(min_length=3, max_length=64)
    preferred_language = serializers.CharField(min_length=2, max_length=40)
    organization_name = serializers.CharField(min_length=2, max_length=140)
    professional_summary = serializers.CharField(min_length=30, max_length=500)
    terms_version = serializers.CharField(max_length=40)
    accepts_synthetic_only = serializers.BooleanField(write_only=True)
    details = serializers.JSONField()

    def validate_email(self, value):
        if not SYNTHETIC_EMAIL_PATTERN.fullmatch(value.strip()):
            raise serializers.ValidationError(
                "Prototype registration accepts fictional .test email addresses only."
            )
        return value.strip().lower()

    def validate_terms_version(self, value):
        if value != TERMS_VERSION:
            raise serializers.ValidationError("Refresh the form and review the current terms.")
        return value

    def validate_accepts_synthetic_only(self, value):
        if not value:
            raise serializers.ValidationError(
                "Confirm that every submitted field is fictional prototype data."
            )
        return value

    def validate(self, attrs):
        application_type = attrs["application_type"]
        details = attrs["details"]
        if not isinstance(details, dict):
            raise serializers.ValidationError({"details": "Details must be a JSON object."})
        if application_type == ApplicationType.DOCTOR:
            attrs["details"] = self._validate_doctor_details(details)
        else:
            attrs["details"] = self._validate_hospital_details(details)
        attrs.pop("accepts_synthetic_only")
        return attrs

    def _validate_doctor_details(self, details):
        serializer = DoctorDetailsSerializer(data=details)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def _validate_hospital_details(self, details):
        serializer = HospitalDetailsSerializer(data=details)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data


class DoctorDetailsSerializer(serializers.Serializer):
    professional_role = serializers.ChoiceField(choices=["referrer", "specialist"])
    primary_specialty = serializers.CharField(min_length=2, max_length=80)
    subspecialties = serializers.ListField(
        child=serializers.CharField(min_length=2, max_length=80),
        min_length=1,
        max_length=8,
    )
    current_designation = serializers.CharField(min_length=2, max_length=100)
    experience_start_year = serializers.IntegerField(min_value=1950, max_value=date.today().year)
    council_jurisdiction = serializers.CharField(min_length=2, max_length=100)
    synthetic_registration_number = serializers.CharField(max_length=80)
    qualifications = serializers.ListField(
        child=serializers.CharField(min_length=2, max_length=120),
        min_length=1,
        max_length=8,
    )
    languages = serializers.ListField(
        child=serializers.CharField(min_length=2, max_length=40),
        min_length=1,
        max_length=10,
    )

    def validate_synthetic_registration_number(self, value):
        value = value.strip().upper()
        if not SYNTHETIC_REGISTRATION_PATTERN.fullmatch(value):
            raise serializers.ValidationError(
                "Use a fictional registration identifier beginning with SYN-."
            )
        return value


class HospitalDetailsSerializer(serializers.Serializer):
    organization_type = serializers.ChoiceField(
        choices=["multi_specialty", "single_specialty", "clinic", "hospital_group"]
    )
    representative_title = serializers.CharField(min_length=2, max_length=100)
    website_url = serializers.URLField(max_length=240)
    establishment_year = serializers.IntegerField(min_value=1900, max_value=date.today().year)
    departments = serializers.ListField(
        child=serializers.CharField(min_length=2, max_length=80),
        min_length=1,
        max_length=20,
    )
    accreditation_labels = serializers.ListField(
        child=serializers.CharField(min_length=2, max_length=80),
        max_length=10,
    )
    bed_count = serializers.IntegerField(min_value=1, max_value=10000)
    capacity_as_of = serializers.DateField()
    international_patient_services = serializers.ListField(
        child=serializers.CharField(min_length=2, max_length=100),
        max_length=12,
    )
    languages = serializers.ListField(
        child=serializers.CharField(min_length=2, max_length=40),
        min_length=1,
        max_length=15,
    )

    def validate_website_url(self, value):
        hostname = (urlparse(value).hostname or "").lower()
        if hostname != "example" and not hostname.endswith(".example"):
            raise serializers.ValidationError(
                "Prototype registration accepts fictional .example websites only."
            )
        return value

    def validate_capacity_as_of(self, value):
        if value > date.today():
            raise serializers.ValidationError("Capacity date cannot be in the future.")
        return value


class PartnerApplicationReviewSerializer(serializers.ModelSerializer):
    application_type_label = serializers.CharField(
        source="get_application_type_display", read_only=True
    )
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    review_reason_label = serializers.CharField(
        source="get_review_reason_code_display", read_only=True
    )
    reviewer_name = serializers.SerializerMethodField()
    activated_organization = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()

    class Meta:
        model = PartnerApplication
        fields = [
            "id",
            "application_type",
            "application_type_label",
            "status",
            "status_label",
            "normalized_email",
            "legal_name",
            "display_name",
            "country",
            "city",
            "timezone",
            "preferred_language",
            "organization_name",
            "professional_summary",
            "terms_version",
            "terms_accepted_at",
            "is_synthetic",
            "reviewer_name",
            "reviewed_at",
            "review_reason_code",
            "review_reason_label",
            "reviewer_note",
            "activated_at",
            "activated_organization",
            "details",
            "created_at",
            "updated_at",
        ]

    def get_reviewer_name(self, instance):
        if instance.reviewer_id is None:
            return None
        profile = getattr(instance.reviewer, "identity_profile", None)
        return profile.display_name if profile else "Platform reviewer"

    def get_activated_organization(self, instance):
        if instance.activated_organization_id is None:
            return None
        return {
            "id": str(instance.activated_organization_id),
            "name": instance.activated_organization.name,
            "slug": instance.activated_organization.slug,
            "type": instance.activated_organization.organization_type,
        }

    def get_details(self, instance):
        if instance.application_type == ApplicationType.DOCTOR:
            details = instance.doctor_details
            return {
                "professional_role": details.professional_role,
                "primary_specialty": details.primary_specialty,
                "subspecialties": details.subspecialties,
                "current_designation": details.current_designation,
                "experience_start_year": details.experience_start_year,
                "council_jurisdiction": details.council_jurisdiction,
                "synthetic_registration_number": details.synthetic_registration_number,
                "qualifications": details.qualifications,
                "languages": details.languages,
            }
        details = instance.hospital_details
        return {
            "organization_type": details.organization_type,
            "representative_title": details.representative_title,
            "website_url": details.website_url,
            "establishment_year": details.establishment_year,
            "departments": details.departments,
            "accreditation_labels": details.accreditation_labels,
            "bed_count": details.bed_count,
            "capacity_as_of": details.capacity_as_of,
            "international_patient_services": details.international_patient_services,
            "languages": details.languages,
        }


class PartnerApplicationReviewListSerializer(serializers.ModelSerializer):
    application_type_label = serializers.CharField(
        source="get_application_type_display", read_only=True
    )
    status_label = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = PartnerApplication
        fields = [
            "id",
            "application_type",
            "application_type_label",
            "status",
            "status_label",
            "display_name",
            "organization_name",
            "country",
            "city",
            "reviewed_at",
            "created_at",
            "updated_at",
        ]


class ApplicationReviewActionSerializer(serializers.Serializer):
    reason_code = serializers.ChoiceField(
        choices=ReviewReason.choices,
        required=False,
        allow_blank=True,
    )
    reviewer_note = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
        trim_whitespace=True,
    )

    def validate(self, attrs):
        action = self.context["action"]
        if action in {"request_changes", "reject"} and not attrs.get("reason_code"):
            raise serializers.ValidationError(
                {"reason_code": "Choose a bounded reason before this action."}
            )
        if action not in {"request_changes", "reject"}:
            attrs["reason_code"] = ""
        return attrs
