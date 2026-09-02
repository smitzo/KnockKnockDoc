import re

from django.db.models import Avg, Count
from rest_framework import serializers

from ..models import (
    ConnectionPurpose,
    ProfessionalConnection,
    ProfessionalConversation,
    ProfessionalDirectoryProfile,
    ProfessionalMessage,
)


SENSITIVE_PATTERN = re.compile(
    r"(?:https?://|\bmrn\b|\bmedical record number\b|\bpassport\b|"
    r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|\+?\d[\d\s().-]{7,}\d)",
    flags=re.IGNORECASE,
)


def reject_sensitive_text(value):
    value = value.strip()
    if SENSITIVE_PATTERN.search(value):
        raise serializers.ValidationError(
            "Keep this professional chat fictional and free of patient identifiers, contact "
            "details, links, and record numbers. Patient-specific work belongs in a scoped case."
        )
    return value


class ProfessionalCardSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(
        source="user.identity_profile.display_name",
        read_only=True,
    )
    professional_role_label = serializers.CharField(
        source="get_professional_role_display", read_only=True
    )
    verification_label = serializers.CharField(
        source="get_verification_state_display", read_only=True
    )
    avatar_url = serializers.SerializerMethodField()
    rating_average = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    rating_breakdown = serializers.SerializerMethodField()

    class Meta:
        model = ProfessionalDirectoryProfile
        fields = [
            "id",
            "display_name",
            "professional_role",
            "professional_role_label",
            "specialty",
            "experience_years",
            "country",
            "city",
            "organization_name",
            "languages",
            "professional_summary",
            "verification_state",
            "verification_label",
            "avatar_url",
            "rating_average",
            "rating_count",
            "rating_breakdown",
            "accepts_connections",
            "is_synthetic",
        ]

    def get_avatar_url(self, instance):
        return f"/demo/avatar/{instance.avatar_key}"

    def _ratings(self, instance):
        cached = getattr(instance, "_serialized_rating_summary", None)
        if cached is not None:
            return cached
        if hasattr(instance, "rating_count_value"):
            values = {
                "count": instance.rating_count_value,
                "communication": instance.communication_rating,
                "collaboration": instance.collaboration_rating,
                "handback": instance.handback_rating,
            }
        else:
            values = instance.ratings.aggregate(
                count=Count("id"),
                communication=Avg("communication_score"),
                collaboration=Avg("collaboration_score"),
                handback=Avg("handback_score"),
            )
        scores = [values[key] for key in ["communication", "collaboration", "handback"]]
        values["average"] = (
            round(sum(float(score) for score in scores) / 3, 1)
            if values["count"] and all(score is not None for score in scores)
            else None
        )
        instance._serialized_rating_summary = values
        return values

    def get_rating_average(self, instance):
        return self._ratings(instance)["average"]

    def get_rating_count(self, instance):
        return self._ratings(instance)["count"]

    def get_rating_breakdown(self, instance):
        values = self._ratings(instance)
        if not values["count"]:
            return None
        return {
            "communication": round(float(values["communication"]), 1),
            "collaboration": round(float(values["collaboration"]), 1),
            "handback": round(float(values["handback"]), 1),
            "scope": "synthetic_peer_collaboration_not_clinical_quality",
        }


class ConnectionCreateSerializer(serializers.Serializer):
    recipient_profile_id = serializers.UUIDField()
    purpose = serializers.ChoiceField(choices=ConnectionPurpose.choices)
    note = serializers.CharField(max_length=400, allow_blank=True, required=False)
    accepts_synthetic_only = serializers.BooleanField()

    def validate_note(self, value):
        return reject_sensitive_text(value) if value else ""

    def validate_accepts_synthetic_only(self, value):
        if not value:
            raise serializers.ValidationError(
                "Confirm that the request contains fictional data only."
            )
        return value


class ConnectionSerializer(serializers.ModelSerializer):
    requester = serializers.SerializerMethodField()
    recipient = serializers.SerializerMethodField()
    peer = serializers.SerializerMethodField()
    viewer_relation = serializers.SerializerMethodField()
    purpose_label = serializers.CharField(source="get_purpose_display", read_only=True)
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    conversation_id = serializers.SerializerMethodField()

    class Meta:
        model = ProfessionalConnection
        fields = [
            "id",
            "requester",
            "recipient",
            "peer",
            "viewer_relation",
            "purpose",
            "purpose_label",
            "note",
            "status",
            "status_label",
            "conversation_id",
            "created_at",
            "responded_at",
        ]

    def get_requester(self, instance):
        return ProfessionalCardSerializer(instance.requester.professional_directory_profile).data

    def get_recipient(self, instance):
        return ProfessionalCardSerializer(instance.recipient.professional_directory_profile).data

    def get_peer(self, instance):
        request = self.context.get("request")
        if request is None:
            return None
        peer = instance.recipient if instance.requester_id == request.user.id else instance.requester
        return ProfessionalCardSerializer(peer.professional_directory_profile).data

    def get_viewer_relation(self, instance):
        request = self.context.get("request")
        if request is None:
            return None
        return "requester" if instance.requester_id == request.user.id else "recipient"

    def get_conversation_id(self, instance):
        try:
            return instance.conversation.id
        except ProfessionalConversation.DoesNotExist:
            return None


class ConversationSerializer(serializers.ModelSerializer):
    connection = ConnectionSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ProfessionalConversation
        fields = ["id", "connection", "last_message", "created_at", "updated_at"]

    def get_last_message(self, instance):
        message = instance.messages.select_related("sender__identity_profile").last()
        return (
            MessageSerializer(message, context={"request": self.context.get("request")}).data
            if message
            else None
        )


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(
        source="sender.identity_profile.display_name",
        read_only=True,
    )
    is_mine = serializers.SerializerMethodField()

    class Meta:
        model = ProfessionalMessage
        fields = ["id", "sender_name", "body", "created_at", "is_mine"]

    def get_is_mine(self, instance):
        request = self.context.get("request")
        return bool(request and request.user.id == instance.sender_id)


class MessageCreateSerializer(serializers.Serializer):
    body = serializers.CharField(min_length=1, max_length=1200)
    accepts_synthetic_only = serializers.BooleanField()

    def validate_body(self, value):
        return reject_sensitive_text(value)

    def validate_accepts_synthetic_only(self, value):
        if not value:
            raise serializers.ValidationError(
                "Confirm that this message is fictional and case-free."
            )
        return value
