from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.demo_lab.fixtures import load_product_demo_fixture
from apps.referrals.models import (
    CaseEvent,
    CaseParticipant,
    InformationRequest,
    ProviderResponse,
    RecordItem,
    ReferralCase,
)


class Command(BaseCommand):
    help = "Load the stable synthetic referral workspace from the versioned JSON fixture."

    @transaction.atomic
    def handle(self, *args, **options):
        fixture = load_product_demo_fixture().referral_workspace
        now = timezone.now()
        referral, _created = ReferralCase.objects.update_or_create(
            reference=fixture["reference"],
            defaults={
                "patient_alias": fixture["patient_alias"],
                "patient_country": fixture["patient_country"],
                "patient_age_band": fixture["patient_age_band"],
                "specialty": fixture["specialty"],
                "clinical_question": fixture["clinical_question"],
                "summary": fixture["summary"],
                "status": fixture["status"],
                "consent_status": fixture["consent_status"],
                "is_planned_care": fixture["is_planned_care"],
                "is_synthetic": fixture["is_synthetic"],
                "corridor_label": fixture["corridor_label"],
                "next_action": fixture["next_action"],
                "next_action_owner": fixture["next_action_owner"],
                "next_action_due": now + timedelta(days=fixture["next_action_due_days"]),
            },
        )
        referral.participants.all().delete()
        referral.records.all().delete()
        referral.information_requests.all().delete()
        referral.responses.all().delete()
        referral.events.all().delete()

        CaseParticipant.objects.bulk_create(
            [CaseParticipant(case=referral, **item) for item in fixture["participants"]]
        )
        RecordItem.objects.bulk_create(
            [
                RecordItem(
                    case=referral,
                    label=item["label"],
                    category=item["category"],
                    clinical_date=date.today()
                    - timedelta(days=item["clinical_date_days_ago"]),
                    source_label=item["source_label"],
                    state=item["state"],
                    note=item["note"],
                )
                for item in fixture["records"]
            ]
        )
        InformationRequest.objects.bulk_create(
            [
                InformationRequest(
                    case=referral,
                    item=item["item"],
                    reason=item["reason"],
                    requester_name=item["requester_name"],
                    requester_role=item["requester_role"],
                    state=item["state"],
                    is_blocking=item["is_blocking"],
                    due_at=now + timedelta(days=item["due_days"]),
                    response_note=item["response_note"],
                )
                for item in fixture["information_requests"]
            ]
        )
        ProviderResponse.objects.bulk_create(
            [
                ProviderResponse(
                    case=referral,
                    response_type=item["response_type"],
                    title=item["title"],
                    author_name=item["author_name"],
                    author_role=item["author_role"],
                    organization=item["organization"],
                    summary=item["summary"],
                    limitations=item["limitations"],
                    state=item["state"],
                    issued_at=now - timedelta(hours=item["issued_hours_ago"]),
                    version=item["version"],
                )
                for item in fixture["responses"]
            ]
        )
        CaseEvent.objects.bulk_create(
            [
                CaseEvent(
                    case=referral,
                    event_type=item["event_type"],
                    actor_label=item["actor_label"],
                    actor_role=item["actor_role"],
                    summary=item["summary"],
                    occurred_at=now
                    - timedelta(
                        days=item.get("occurred_days_ago", 0),
                        hours=item.get("occurred_hours_ago", 0),
                    ),
                )
                for item in fixture["events"]
            ]
        )
        self.stdout.write(self.style.SUCCESS(f"Seeded synthetic workspace {referral.reference}"))
