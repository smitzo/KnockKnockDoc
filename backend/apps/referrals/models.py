from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone

from apps.core.models import UUIDTimeStampedModel
from apps.identity.models import OrganizationMembership


class CaseStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    AWAITING_CONSENT = "awaiting_consent", "Awaiting consent"
    COMPLETENESS_REVIEW = "completeness_review", "Completeness review"
    READY_TO_ROUTE = "ready_to_route", "Ready to route"
    PROVIDER_REVIEW = "provider_review", "Provider review"
    INFORMATION_REQUIRED = "information_required", "Information required"
    RESPONSE_READY = "response_ready", "Response ready"
    PATIENT_DECISION = "patient_decision", "Patient decision"
    PREPARING_TRAVEL = "preparing_travel", "Preparing travel"
    TREATMENT = "treatment", "Treatment"
    HANDBACK = "handback", "Handback"
    CLOSED = "closed", "Closed"


class ConsentStatus(models.TextChoices):
    NOT_REQUESTED = "not_requested", "Not requested"
    PENDING = "pending", "Pending"
    GRANTED = "granted", "Granted"
    DECLINED = "declined", "Declined"
    WITHDRAWN = "withdrawn", "Withdrawn"


class ReferralCase(UUIDTimeStampedModel):
    reference = models.CharField(max_length=24, unique=True)
    patient_alias = models.CharField(max_length=80)
    patient_country = models.CharField(max_length=80)
    patient_age_band = models.CharField(max_length=30)
    specialty = models.CharField(max_length=80)
    clinical_question = models.CharField(max_length=500)
    summary = models.TextField(max_length=2000)
    status = models.CharField(max_length=32, choices=CaseStatus.choices, default=CaseStatus.DRAFT)
    consent_status = models.CharField(
        max_length=24,
        choices=ConsentStatus.choices,
        default=ConsentStatus.NOT_REQUESTED,
    )
    is_planned_care = models.BooleanField(default=True)
    is_synthetic = models.BooleanField(default=True)
    corridor_label = models.CharField(max_length=120, default="Illustrative corridor")
    next_action = models.CharField(max_length=280)
    next_action_owner = models.CharField(max_length=100)
    next_action_due = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.CheckConstraint(condition=Q(is_synthetic=True), name="prototype_cases_synthetic"),
            models.CheckConstraint(condition=Q(is_planned_care=True), name="prototype_planned_care"),
        ]
        indexes = [
            models.Index(fields=["status", "next_action_due"], name="ref_case_queue_idx"),
            models.Index(fields=["updated_at"], name="ref_case_updated_idx"),
        ]

    def __str__(self) -> str:
        return self.reference


class AssignmentStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    ENDED = "ended", "Ended"


class CaseAssignment(UUIDTimeStampedModel):
    case = models.ForeignKey(
        ReferralCase,
        related_name="assignments",
        on_delete=models.CASCADE,
    )
    membership = models.ForeignKey(
        OrganizationMembership,
        related_name="case_assignments",
        on_delete=models.PROTECT,
    )
    purpose = models.CharField(max_length=180)
    status = models.CharField(
        max_length=16,
        choices=AssignmentStatus.choices,
        default=AssignmentStatus.ACTIVE,
    )
    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["case", "membership"],
                name="unique_case_membership_assignment",
            ),
            models.CheckConstraint(
                condition=Q(ends_at__isnull=True) | Q(ends_at__gt=models.F("starts_at")),
                name="assignment_end_after_start",
            ),
        ]
        indexes = [
            models.Index(fields=["membership", "status"], name="ref_assignment_member_idx"),
            models.Index(fields=["case", "status"], name="ref_assignment_case_idx"),
        ]


class AccessScope(models.TextChoices):
    CASE_VIEW = "case:view", "View case"
    CASE_EDIT = "case:edit", "Edit case"
    CASE_MANAGE = "case:manage", "Manage case access"
    RECORDS_VIEW = "records:view", "View shared record metadata"
    RESPONSE_ISSUE = "response:issue", "Issue a provider response"


class CaseAccessGrant(UUIDTimeStampedModel):
    assignment = models.ForeignKey(
        CaseAssignment,
        related_name="grants",
        on_delete=models.PROTECT,
    )
    purpose = models.CharField(max_length=180)
    granted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="case_grants_issued",
        on_delete=models.PROTECT,
    )
    granted_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    revoked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="case_grants_revoked",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    revocation_reason = models.CharField(max_length=180, blank=True)

    class Meta:
        ordering = ["-granted_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["assignment"],
                condition=Q(revoked_at__isnull=True),
                name="one_current_grant_per_assignment",
            ),
            models.CheckConstraint(
                condition=Q(expires_at__isnull=True) | Q(expires_at__gt=models.F("granted_at")),
                name="grant_expiry_after_grant",
            ),
        ]
        indexes = [
            models.Index(fields=["assignment", "revoked_at"], name="ref_grant_assignment_idx"),
            models.Index(fields=["expires_at"], name="ref_grant_expiry_idx"),
        ]


class GrantScope(UUIDTimeStampedModel):
    grant = models.ForeignKey(
        CaseAccessGrant,
        related_name="scopes",
        on_delete=models.CASCADE,
    )
    scope = models.CharField(max_length=40, choices=AccessScope.choices)

    class Meta:
        ordering = ["scope"]
        constraints = [
            models.UniqueConstraint(
                fields=["grant", "scope"],
                name="unique_grant_scope",
            )
        ]
        indexes = [models.Index(fields=["scope", "grant"], name="ref_scope_lookup_idx")]


class ParticipantRole(models.TextChoices):
    PATIENT = "patient", "Patient"
    REFERRER = "referrer", "Referring doctor"
    SPECIALIST = "specialist", "Receiving specialist"
    HOSPITAL = "hospital", "Hospital team"
    COORDINATOR = "coordinator", "Care coordinator"


class AccessState(models.TextChoices):
    ACTIVE = "active", "Active"
    PENDING = "pending", "Pending"
    REVOKED = "revoked", "Revoked"


class CaseParticipant(UUIDTimeStampedModel):
    case = models.ForeignKey(ReferralCase, related_name="participants", on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)
    role = models.CharField(max_length=24, choices=ParticipantRole.choices)
    organization = models.CharField(max_length=120, blank=True)
    access_scope = models.CharField(max_length=240)
    access_state = models.CharField(
        max_length=16,
        choices=AccessState.choices,
        default=AccessState.ACTIVE,
    )
    purpose = models.CharField(max_length=160)

    class Meta:
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["case", "display_name", "role"], name="unique_case_participant_label"
            )
        ]


class RecordState(models.TextChoices):
    READY = "ready", "Ready"
    NEEDS_UPDATE = "needs_update", "Needs update"
    REQUESTED = "requested", "Requested"
    UNAVAILABLE = "unavailable", "Unavailable"


class RecordItem(UUIDTimeStampedModel):
    case = models.ForeignKey(ReferralCase, related_name="records", on_delete=models.CASCADE)
    label = models.CharField(max_length=140)
    category = models.CharField(max_length=80)
    clinical_date = models.DateField(null=True, blank=True)
    source_label = models.CharField(max_length=120)
    state = models.CharField(max_length=20, choices=RecordState.choices)
    note = models.CharField(max_length=240, blank=True)

    class Meta:
        ordering = ["-clinical_date", "created_at"]


class RequestState(models.TextChoices):
    OPEN = "open", "Open"
    ANSWERED = "answered", "Answered"
    UNAVAILABLE = "unavailable", "Unavailable"


class InformationRequest(UUIDTimeStampedModel):
    case = models.ForeignKey(
        ReferralCase,
        related_name="information_requests",
        on_delete=models.CASCADE,
    )
    item = models.CharField(max_length=180)
    reason = models.CharField(max_length=280)
    requester_name = models.CharField(max_length=100)
    requester_role = models.CharField(max_length=80)
    state = models.CharField(max_length=20, choices=RequestState.choices, default=RequestState.OPEN)
    is_blocking = models.BooleanField(default=False)
    due_at = models.DateTimeField(null=True, blank=True)
    response_note = models.CharField(max_length=280, blank=True)

    class Meta:
        ordering = ["state", "due_at"]


class ResponseType(models.TextChoices):
    CLINICAL_OPINION = "clinical_opinion", "Clinical opinion"
    COORDINATION_PLAN = "coordination_plan", "Coordination plan"
    INDICATIVE_QUOTE = "indicative_quote", "Indicative quote"


class ResponseState(models.TextChoices):
    DRAFT = "draft", "Draft"
    ISSUED = "issued", "Issued"
    SUPERSEDED = "superseded", "Superseded"


class ProviderResponse(UUIDTimeStampedModel):
    case = models.ForeignKey(ReferralCase, related_name="responses", on_delete=models.CASCADE)
    response_type = models.CharField(max_length=32, choices=ResponseType.choices)
    title = models.CharField(max_length=160)
    author_name = models.CharField(max_length=100)
    author_role = models.CharField(max_length=100)
    organization = models.CharField(max_length=140)
    summary = models.TextField(max_length=1600)
    limitations = models.TextField(max_length=800)
    state = models.CharField(max_length=20, choices=ResponseState.choices)
    issued_at = models.DateTimeField(null=True, blank=True)
    version = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["-issued_at", "-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["case", "response_type", "version"], name="unique_case_response_version"
            )
        ]


class CaseEvent(UUIDTimeStampedModel):
    case = models.ForeignKey(ReferralCase, related_name="events", on_delete=models.CASCADE)
    event_type = models.CharField(max_length=60)
    actor_label = models.CharField(max_length=100)
    actor_role = models.CharField(max_length=80)
    summary = models.CharField(max_length=280)
    occurred_at = models.DateTimeField()

    class Meta:
        ordering = ["-occurred_at", "-created_at"]
        indexes = [models.Index(fields=["case", "-occurred_at"], name="ref_event_timeline_idx")]
