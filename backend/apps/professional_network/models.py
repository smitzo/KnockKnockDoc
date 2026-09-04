import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q
from django.utils import timezone

from apps.core.models import UUIDTimeStampedModel


class ProfessionalRole(models.TextChoices):
    REFERRER = "referrer", "Referring doctor"
    SPECIALIST = "specialist", "Receiving specialist"


class VerificationState(models.TextChoices):
    SYNTHETIC_VERIFIED = "synthetic_verified", "Synthetic verified"
    SYNTHETIC_ADMIN_REVIEW = "synthetic_admin_review", "Synthetic admin review"


class ProfessionalDirectoryProfile(UUIDTimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="professional_directory_profile",
        on_delete=models.PROTECT,
    )
    professional_role = models.CharField(max_length=24, choices=ProfessionalRole.choices)
    specialty = models.CharField(max_length=80)
    experience_years = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    organization_name = models.CharField(max_length=140)
    languages = models.JSONField(default=list)
    professional_summary = models.CharField(max_length=500)
    avatar_key = models.CharField(max_length=40)
    verification_state = models.CharField(
        max_length=32,
        choices=VerificationState.choices,
        default=VerificationState.SYNTHETIC_VERIFIED,
    )
    is_discoverable = models.BooleanField(default=True)
    accepts_connections = models.BooleanField(default=True)
    is_synthetic = models.BooleanField(default=True)

    class Meta:
        ordering = ["user__identity_profile__display_name"]
        constraints = [
            models.CheckConstraint(
                condition=Q(is_synthetic=True),
                name="network_profile_synthetic",
            )
        ]
        indexes = [
            models.Index(
                fields=["is_discoverable", "specialty"],
                name="network_profile_specialty_idx",
            ),
            models.Index(fields=["country", "city"], name="network_profile_location_idx"),
        ]

    def __str__(self):
        return self.user.identity_profile.display_name


class ProfessionalRating(UUIDTimeStampedModel):
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="given_professional_ratings",
        on_delete=models.PROTECT,
    )
    subject = models.ForeignKey(
        ProfessionalDirectoryProfile,
        related_name="ratings",
        on_delete=models.PROTECT,
    )
    communication_score = models.PositiveSmallIntegerField()
    collaboration_score = models.PositiveSmallIntegerField()
    handback_score = models.PositiveSmallIntegerField()
    comment = models.CharField(max_length=320, blank=True)
    is_synthetic = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["reviewer", "subject"],
                name="network_unique_reviewer_subject",
            ),
            models.CheckConstraint(
                condition=Q(communication_score__gte=1, communication_score__lte=5),
                name="network_rating_communication_range",
            ),
            models.CheckConstraint(
                condition=Q(collaboration_score__gte=1, collaboration_score__lte=5),
                name="network_rating_collaboration_range",
            ),
            models.CheckConstraint(
                condition=Q(handback_score__gte=1, handback_score__lte=5),
                name="network_rating_handback_range",
            ),
            models.CheckConstraint(
                condition=Q(is_synthetic=True),
                name="network_rating_synthetic",
            ),
        ]
        indexes = [
            models.Index(fields=["subject", "-created_at"], name="network_rating_subject_idx")
        ]


class ConnectionPurpose(models.TextChoices):
    REFERRAL_COLLABORATION = "referral_collaboration", "Referral collaboration"
    SECOND_OPINION_PATHWAY = "second_opinion_pathway", "Second-opinion pathway"
    HANDBACK_COORDINATION = "handback_coordination", "Home-doctor handback"
    PROFESSIONAL_INTRODUCTION = "professional_introduction", "Professional introduction"


class ConnectionStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    DECLINED = "declined", "Declined"
    WITHDRAWN = "withdrawn", "Withdrawn"


class ProfessionalConnection(UUIDTimeStampedModel):
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="sent_professional_connections",
        on_delete=models.PROTECT,
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_professional_connections",
        on_delete=models.PROTECT,
    )
    pair_key = models.CharField(max_length=50, unique=True, editable=False)
    purpose = models.CharField(max_length=40, choices=ConnectionPurpose.choices)
    note = models.CharField(max_length=400, blank=True)
    status = models.CharField(
        max_length=16,
        choices=ConnectionStatus.choices,
        default=ConnectionStatus.PENDING,
    )
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=~Q(requester=F("recipient")),
                name="network_connection_distinct_users",
            )
        ]
        indexes = [
            models.Index(fields=["requester", "status"], name="network_connection_request_idx"),
            models.Index(fields=["recipient", "status"], name="network_connection_receive_idx"),
        ]

    @staticmethod
    def build_pair_key(first_user_id: int, second_user_id: int) -> str:
        low, high = sorted([int(first_user_id), int(second_user_id)])
        return f"{low}:{high}"

    def save(self, *args, **kwargs):
        if self.requester_id and self.recipient_id:
            self.pair_key = self.build_pair_key(self.requester_id, self.recipient_id)
        super().save(*args, **kwargs)


class ProfessionalConversation(UUIDTimeStampedModel):
    connection = models.OneToOneField(
        ProfessionalConnection,
        related_name="conversation",
        on_delete=models.PROTECT,
    )

    class Meta:
        ordering = ["-updated_at"]


class ImmutableMessageQuerySet(models.QuerySet):
    def update(self, **kwargs):
        raise ValidationError("Professional messages are append-only.")

    def delete(self):
        raise ValidationError("Professional messages are append-only.")


class ProfessionalMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        ProfessionalConversation,
        related_name="messages",
        on_delete=models.PROTECT,
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="professional_messages",
        on_delete=models.PROTECT,
    )
    body = models.CharField(max_length=1200)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    objects = ImmutableMessageQuerySet.as_manager()

    class Meta:
        ordering = ["created_at", "id"]
        indexes = [
            models.Index(fields=["conversation", "created_at"], name="network_message_thread_idx")
        ]

    def save(self, *args, **kwargs):
        if not self._state.adding:
            raise ValidationError("Professional messages are append-only.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Professional messages are append-only.")
