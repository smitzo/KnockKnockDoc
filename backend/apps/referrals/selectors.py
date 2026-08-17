from django.db.models import Prefetch, QuerySet

from .models import (
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
