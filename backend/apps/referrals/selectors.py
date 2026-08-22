from django.db.models import Prefetch, Q, QuerySet, Subquery
from django.utils import timezone

from apps.identity.models import MembershipRole, OrganizationMembership
from apps.identity.selectors import active_memberships_for_user

from .models import (
    AccessScope,
    AssignmentStatus,
    CaseAssignment,
    CaseEvent,
    InformationRequest,
    ProviderResponse,
    RecordItem,
    ReferralCase,
)

DEMO_REFERENCE = "KND-DEMO-001"


def referral_workspace_queryset() -> QuerySet[ReferralCase]:
    return ReferralCase.objects.prefetch_related(
        "participants",
        Prefetch("records", queryset=RecordItem.objects.order_by("-clinical_date", "created_at")),
        Prefetch(
            "information_requests",
            queryset=InformationRequest.objects.order_by("state", "due_at"),
        ),
        Prefetch("responses", queryset=ProviderResponse.objects.order_by("-issued_at")),
        Prefetch("events", queryset=CaseEvent.objects.order_by("-occurred_at")),
    )


def get_demo_workspace() -> ReferralCase:
    return referral_workspace_queryset().get(reference=DEMO_REFERENCE, is_synthetic=True)


def accessible_referrals(user, scope: str = AccessScope.CASE_VIEW) -> QuerySet[ReferralCase]:
    if not user or not user.is_authenticated:
        return ReferralCase.objects.none()

    now = timezone.now()
    membership_ids = active_memberships_for_user(user).order_by().values("id")
    access_filter = (
        Q(assignments__membership_id__in=Subquery(membership_ids))
        & Q(assignments__status=AssignmentStatus.ACTIVE)
        & Q(assignments__starts_at__lte=now)
        & (Q(assignments__ends_at__isnull=True) | Q(assignments__ends_at__gt=now))
        & Q(assignments__grants__granted_at__lte=now)
        & Q(assignments__grants__revoked_at__isnull=True)
        & (
            Q(assignments__grants__expires_at__isnull=True)
            | Q(assignments__grants__expires_at__gt=now)
        )
        & Q(assignments__grants__scopes__scope=scope)
    )
    return ReferralCase.objects.filter(access_filter).distinct()


def authorized_referral_workspace_queryset(
    user,
    scope: str = AccessScope.CASE_VIEW,
) -> QuerySet[ReferralCase]:
    accessible_case_ids = accessible_referrals(user, scope).order_by().values("id")
    return referral_workspace_queryset().filter(id__in=Subquery(accessible_case_ids))


def authorized_membership_for_case(
    user,
    case: ReferralCase,
    scope: str = AccessScope.CASE_VIEW,
) -> OrganizationMembership | None:
    if not user or not user.is_authenticated:
        return None

    now = timezone.now()
    active_membership_ids = active_memberships_for_user(user).order_by().values("id")
    assignment = (
        CaseAssignment.objects.select_related(
            "membership__organization",
            "membership__user__identity_profile",
        )
        .filter(
            Q(case=case)
            & Q(membership_id__in=Subquery(active_membership_ids))
            & Q(status=AssignmentStatus.ACTIVE)
            & Q(starts_at__lte=now)
            & (Q(ends_at__isnull=True) | Q(ends_at__gt=now))
            & Q(grants__granted_at__lte=now)
            & Q(grants__revoked_at__isnull=True)
            & (Q(grants__expires_at__isnull=True) | Q(grants__expires_at__gt=now))
            & Q(grants__scopes__scope=scope)
        )
        .order_by("created_at")
        .first()
    )
    return assignment.membership if assignment else None


def active_referrer_memberships(user) -> QuerySet[OrganizationMembership]:
    return active_memberships_for_user(user).filter(role=MembershipRole.REFERRER)
