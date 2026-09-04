import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone

from apps.core.models import UUIDTimeStampedModel


class OrganizationType(models.TextChoices):
    PLATFORM = "platform", "Platform"
    HOSPITAL = "hospital", "Hospital"
    REFERRING_PRACTICE = "referring_practice", "Referring practice"


class OrganizationStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    SUSPENDED = "suspended", "Suspended"


class Organization(UUIDTimeStampedModel):
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=80, unique=True)
    organization_type = models.CharField(max_length=32, choices=OrganizationType.choices)
    status = models.CharField(
        max_length=16,
        choices=OrganizationStatus.choices,
        default=OrganizationStatus.ACTIVE,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class AccountType(models.TextChoices):
    PATIENT = "patient", "Patient"
    PROFESSIONAL = "professional", "Professional"
    COORDINATOR = "coordinator", "Coordinator"


class IdentityStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    SUSPENDED = "suspended", "Suspended"


class VerificationBasis(models.TextChoices):
    UNVERIFIED = "unverified", "Unverified"
    SYNTHETIC_FIXTURE = "synthetic_fixture", "Synthetic fixture"
    SYNTHETIC_ADMIN_REVIEW = "synthetic_admin_review", "Synthetic admin review"
    EMAIL_TOKEN = "email_token", "Email token"


class IdentityProfile(UUIDTimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="identity_profile",
        on_delete=models.PROTECT,
    )
    normalized_email = models.EmailField(max_length=254, unique=True)
    display_name = models.CharField(max_length=120)
    account_type = models.CharField(max_length=20, choices=AccountType.choices)
    status = models.CharField(
        max_length=16,
        choices=IdentityStatus.choices,
        default=IdentityStatus.ACTIVE,
    )
    email_verified_at = models.DateTimeField(null=True, blank=True)
    verification_basis = models.CharField(
        max_length=32,
        choices=VerificationBasis.choices,
        default=VerificationBasis.UNVERIFIED,
    )

    class Meta:
        ordering = ["normalized_email"]

    @property
    def is_access_eligible(self) -> bool:
        return bool(
            self.user.is_active
            and self.status == IdentityStatus.ACTIVE
            and self.email_verified_at is not None
            and self.verification_basis != VerificationBasis.UNVERIFIED
        )

    def __str__(self) -> str:
        return self.normalized_email


class MembershipRole(models.TextChoices):
    PATIENT = "patient", "Patient"
    REFERRER = "referrer", "Referring doctor"
    SPECIALIST = "specialist", "Receiving specialist"
    HOSPITAL_COORDINATOR = "hospital_coordinator", "Hospital coordinator"
    PLATFORM_COORDINATOR = "platform_coordinator", "Platform coordinator"
    ADMIN = "admin", "Organization administrator"


class MembershipStatus(models.TextChoices):
    INVITED = "invited", "Invited"
    ACTIVE = "active", "Active"
    SUSPENDED = "suspended", "Suspended"


class OrganizationMembership(UUIDTimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="organization_memberships",
        on_delete=models.PROTECT,
    )
    organization = models.ForeignKey(
        Organization,
        related_name="memberships",
        on_delete=models.PROTECT,
    )
    role = models.CharField(max_length=32, choices=MembershipRole.choices)
    status = models.CharField(
        max_length=16,
        choices=MembershipStatus.choices,
        default=MembershipStatus.INVITED,
    )
    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["organization__name", "role"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "organization", "role"],
                name="unique_user_organization_role",
            ),
            models.CheckConstraint(
                condition=Q(ends_at__isnull=True) | Q(ends_at__gt=models.F("starts_at")),
                name="membership_end_after_start",
            ),
        ]
        indexes = [
            models.Index(fields=["user", "status", "role"], name="identity_member_user_idx"),
            models.Index(fields=["organization", "status"], name="identity_member_org_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.user_id}:{self.organization.slug}:{self.role}"


class SecurityAction(models.TextChoices):
    LOGIN_SUCCEEDED = "auth.login_succeeded", "Login succeeded"
    LOGOUT = "auth.logout", "Logout"
    CASE_VIEWED = "case.viewed", "Case viewed"
    CASE_CREATED = "case.created", "Case created"
    ADMIN_LAB_VIEWED = "admin.lab_viewed", "Admin lab viewed"
    ADMIN_LAB_LOADED = "admin.lab_loaded", "Admin lab demo data loaded"
    ADMIN_LAB_DELETED = "admin.lab_deleted", "Admin lab demo data deleted"
    NETWORK_CONNECTION_REQUESTED = "network.connection_requested", "Connection requested"
    NETWORK_CONNECTION_RESPONDED = "network.connection_responded", "Connection responded"
    NETWORK_MESSAGE_SENT = "network.message_sent", "Professional message sent"
    ONBOARDING_APPLICATION_SUBMITTED = (
        "onboarding.application_submitted",
        "Partner application submitted",
    )
    ONBOARDING_REVIEW_VIEWED = "onboarding.review_viewed", "Application review viewed"
    ONBOARDING_REVIEW_STARTED = "onboarding.review_started", "Application review started"
    ONBOARDING_CHANGES_REQUESTED = (
        "onboarding.changes_requested",
        "Application changes requested",
    )
    ONBOARDING_APPLICATION_APPROVED = (
        "onboarding.application_approved",
        "Application approved",
    )
    ONBOARDING_APPLICATION_REJECTED = (
        "onboarding.application_rejected",
        "Application rejected",
    )


class ImmutableSecurityEventQuerySet(models.QuerySet):
    def update(self, **kwargs):
        raise ValidationError("Security events are append-only.")

    def delete(self):
        raise ValidationError("Security events are append-only.")


class SecurityEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="security_events",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    organization = models.ForeignKey(
        Organization,
        related_name="security_events",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    action = models.CharField(max_length=64, choices=SecurityAction.choices)
    target_type = models.CharField(max_length=64, blank=True)
    target_id = models.UUIDField(null=True, blank=True)
    safe_metadata = models.JSONField(default=dict, blank=True)
    occurred_at = models.DateTimeField(auto_now_add=True)

    objects = ImmutableSecurityEventQuerySet.as_manager()

    class Meta:
        ordering = ["-occurred_at"]
        indexes = [
            models.Index(fields=["actor", "-occurred_at"], name="identity_event_actor_idx"),
            models.Index(fields=["action", "-occurred_at"], name="identity_event_action_idx"),
            models.Index(fields=["target_type", "target_id"], name="identity_event_target_idx"),
        ]

    def save(self, *args, **kwargs):
        if not self._state.adding:
            raise ValidationError("Security events are append-only.")
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Security events are append-only.")
