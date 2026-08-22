import re

from rest_framework import serializers

from ..models import (
    CaseEvent,
    CaseParticipant,
    CaseStatus,
    InformationRequest,
    ProviderResponse,
    RecordItem,
    ReferralCase,
)
from ..services import CreateReferralCommand, create_referral_case

EMERGENCY_PATTERN = re.compile(
    r"\b(emergency|unconscious|cannot breathe|severe bleeding|stroke symptoms|suicidal|"
    r"chest pain now)\b",
    flags=re.IGNORECASE,
)
DIRECT_IDENTIFIER_PATTERN = re.compile(r"(?:@|\+?\d[\d\s()-]{7,}\d)")


class CaseParticipantSerializer(serializers.ModelSerializer):
    role_label = serializers.CharField(source="get_role_display", read_only=True)
    access_state_label = serializers.CharField(source="get_access_state_display", read_only=True)

    class Meta:
        model = CaseParticipant
        fields = [
            "id",
            "display_name",
            "role",
            "role_label",
            "organization",
            "access_scope",
            "access_state",
            "access_state_label",
            "purpose",
        ]


class RecordItemSerializer(serializers.ModelSerializer):
    state_label = serializers.CharField(source="get_state_display", read_only=True)

    class Meta:
        model = RecordItem
        fields = [
            "id",
            "label",
            "category",
            "clinical_date",
            "source_label",
            "state",
            "state_label",
            "note",
        ]


class InformationRequestSerializer(serializers.ModelSerializer):
    state_label = serializers.CharField(source="get_state_display", read_only=True)

    class Meta:
        model = InformationRequest
        fields = [
            "id",
            "item",
            "reason",
            "requester_name",
            "requester_role",
            "state",
            "state_label",
            "is_blocking",
            "due_at",
            "response_note",
        ]


class ProviderResponseSerializer(serializers.ModelSerializer):
    response_type_label = serializers.CharField(source="get_response_type_display", read_only=True)
    state_label = serializers.CharField(source="get_state_display", read_only=True)

    class Meta:
        model = ProviderResponse
        fields = [
            "id",
            "response_type",
            "response_type_label",
            "title",
            "author_name",
            "author_role",
            "organization",
            "summary",
            "limitations",
            "state",
            "state_label",
            "issued_at",
            "version",
        ]


class CaseEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseEvent
        fields = ["id", "event_type", "actor_label", "actor_role", "summary", "occurred_at"]


class ReferralCaseListSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    consent_status_label = serializers.CharField(source="get_consent_status_display", read_only=True)

    class Meta:
        model = ReferralCase
        fields = [
            "id",
            "reference",
            "patient_alias",
            "patient_country",
            "specialty",
            "status",
            "status_label",
            "consent_status",
            "consent_status_label",
            "corridor_label",
            "next_action",
            "next_action_owner",
            "next_action_due",
            "updated_at",
        ]


class ReferralCaseDetailSerializer(ReferralCaseListSerializer):
    participants = CaseParticipantSerializer(many=True, read_only=True)
    records = RecordItemSerializer(many=True, read_only=True)
    information_requests = InformationRequestSerializer(many=True, read_only=True)
    responses = ProviderResponseSerializer(many=True, read_only=True)
    events = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()

    class Meta(ReferralCaseListSerializer.Meta):
        fields = ReferralCaseListSerializer.Meta.fields + [
            "patient_age_band",
            "clinical_question",
            "summary",
            "is_planned_care",
            "is_synthetic",
            "progress_percent",
            "participants",
            "records",
            "information_requests",
            "responses",
            "events",
            "created_at",
        ]

    def get_progress_percent(self, instance: ReferralCase) -> int:
        stages = [status for status, _label in CaseStatus.choices if status != CaseStatus.CLOSED]
        if instance.status == CaseStatus.CLOSED:
            return 100
        try:
            position = stages.index(instance.status)
        except ValueError:
            return 0
        return round((position / max(1, len(stages) - 1)) * 100)

    def get_events(self, instance: ReferralCase):
        return CaseEventSerializer(instance.events.all()[:12], many=True).data


class ReferralCaseCreateSerializer(serializers.Serializer):
    patient_alias = serializers.CharField(min_length=2, max_length=80)
    patient_country = serializers.CharField(min_length=2, max_length=80)
    patient_age_band = serializers.ChoiceField(
        choices=["child", "18–29", "30–44", "45–59", "60–74", "75+"]
    )
    specialty = serializers.ChoiceField(
        choices=["Oncology", "Cardiac sciences", "Complex surgery", "Neurology", "Other"]
    )
    clinical_question = serializers.CharField(min_length=20, max_length=500)
    summary = serializers.CharField(min_length=30, max_length=2000)
    is_planned_care = serializers.BooleanField()
    accepts_synthetic_only = serializers.BooleanField()

    def validate_patient_alias(self, value: str) -> str:
        if DIRECT_IDENTIFIER_PATTERN.search(value):
            raise serializers.ValidationError(
                "Use a synthetic alias only—never enter a phone number or email address."
            )
        return value.strip()

    def validate(self, attrs):
        if not attrs["is_planned_care"]:
            raise serializers.ValidationError(
                {
                    "is_planned_care": (
                        "This prototype coordinates stable, planned care only. For urgent concerns, "
                        "contact local emergency services or a treating clinician now."
                    )
                }
            )
        if not attrs["accepts_synthetic_only"]:
            raise serializers.ValidationError(
                {"accepts_synthetic_only": "Confirm that all information is fictional and synthetic."}
            )
        safety_text = f"{attrs['clinical_question']} {attrs['summary']}"
        if EMERGENCY_PATTERN.search(safety_text):
            raise serializers.ValidationError(
                {
                    "non_field_errors": [
                        "This service is not an emergency or triage service. Contact local emergency "
                        "services or a treating clinician now; do not submit this scenario here."
                    ]
                }
            )
        return attrs

    def create(self, validated_data):
        referrer_membership = validated_data.pop("referrer_membership")
        command = CreateReferralCommand(
            **{
                key: validated_data[key]
                for key in [
                    "patient_alias",
                    "patient_country",
                    "patient_age_band",
                    "specialty",
                    "clinical_question",
                    "summary",
                ]
            }
        )
        return create_referral_case(command, referrer_membership=referrer_membership)
