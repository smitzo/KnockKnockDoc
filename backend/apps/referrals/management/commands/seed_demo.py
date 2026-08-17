from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.referrals.models import (
    AccessState,
    CaseEvent,
    CaseParticipant,
    CaseStatus,
    ConsentStatus,
    InformationRequest,
    ParticipantRole,
    ProviderResponse,
    RecordItem,
    RecordState,
    ReferralCase,
    RequestState,
    ResponseState,
    ResponseType,
)
from apps.referrals.selectors import DEMO_REFERENCE


class Command(BaseCommand):
    help = "Create or refresh the stable, synthetic referral workspace used by Prototype V0."

    @transaction.atomic
    def handle(self, *args, **options):
        now = timezone.now()
        referral, _created = ReferralCase.objects.update_or_create(
            reference=DEMO_REFERENCE,
            defaults={
                "patient_alias": "Ama K. · synthetic",
                "patient_country": "Kenya",
                "patient_age_band": "45–59",
                "specialty": "Oncology",
                "clinical_question": (
                    "Please review the existing pathology and imaging summaries and advise whether "
                    "an in-person specialist assessment in India is appropriate."
                ),
                "summary": (
                    "A fictional planned-care scenario with prior local assessment, organized reports, "
                    "and a home doctor who will remain involved. No real patient information is used."
                ),
                "status": CaseStatus.PATIENT_DECISION,
                "consent_status": ConsentStatus.GRANTED,
                "is_planned_care": True,
                "is_synthetic": True,
                "corridor_label": "Illustrative Kenya → India · Oncology",
                "next_action": "Review the preliminary response with the referring doctor.",
                "next_action_owner": "Ama K. · synthetic",
                "next_action_due": now + timedelta(days=2),
            },
        )
        referral.participants.all().delete()
        referral.records.all().delete()
        referral.information_requests.all().delete()
        referral.responses.all().delete()
        referral.events.all().delete()

        CaseParticipant.objects.bulk_create(
            [
                CaseParticipant(
                    case=referral,
                    display_name="Ama K. · synthetic",
                    role=ParticipantRole.PATIENT,
                    access_scope="Entire patient-visible rehearsal workspace",
                    access_state=AccessState.ACTIVE,
                    purpose="Review and decide on the fictional referral",
                ),
                CaseParticipant(
                    case=referral,
                    display_name="Dr. Lena A. · synthetic",
                    role=ParticipantRole.REFERRER,
                    organization="Nairobi referring practice · fictional",
                    access_scope="Referral packet, clinical response, and handback",
                    access_state=AccessState.ACTIVE,
                    purpose="Maintain the home-clinician care loop",
                ),
                CaseParticipant(
                    case=referral,
                    display_name="Dr. Arun Mehta · synthetic",
                    role=ParticipantRole.SPECIALIST,
                    organization="Aarunya Cancer Centre · fictional",
                    access_scope="Explicitly shared synthetic clinical-record metadata",
                    access_state=AccessState.ACTIVE,
                    purpose="Provide a bounded preliminary review",
                ),
                CaseParticipant(
                    case=referral,
                    display_name="Nila · prototype coordinator",
                    role=ParticipantRole.COORDINATOR,
                    organization="Knock Knock Doc",
                    access_scope="Coordination summary and assigned actions",
                    access_state=AccessState.ACTIVE,
                    purpose="Own the next safe operational step",
                ),
            ]
        )
        RecordItem.objects.bulk_create(
            [
                RecordItem(
                    case=referral,
                    label="Structured referral summary",
                    category="Referral letter",
                    clinical_date=date.today() - timedelta(days=12),
                    source_label="Referring doctor · synthetic",
                    state=RecordState.READY,
                    note="Reviewed for completeness",
                ),
                RecordItem(
                    case=referral,
                    label="Pathology report summary",
                    category="Pathology",
                    clinical_date=date.today() - timedelta(days=28),
                    source_label="Local laboratory · fictional",
                    state=RecordState.READY,
                    note="Original source remains attributable",
                ),
                RecordItem(
                    case=referral,
                    label="CT report summary",
                    category="Radiology report",
                    clinical_date=date.today() - timedelta(days=20),
                    source_label="Local imaging centre · fictional",
                    state=RecordState.READY,
                    note="Still-image upload is not enabled in V0",
                ),
                RecordItem(
                    case=referral,
                    label="Current medicine list",
                    category="Medication",
                    clinical_date=date.today() - timedelta(days=3),
                    source_label="Patient and referrer · synthetic",
                    state=RecordState.NEEDS_UPDATE,
                    note="Add frequency and last-dose dates before travel planning",
                ),
            ]
        )
        InformationRequest.objects.create(
            case=referral,
            item="Medicine frequency and last-dose dates",
            reason="Needed for a complete in-person assessment handoff; not blocking this preliminary review.",
            requester_name="Dr. Arun Mehta · synthetic",
            requester_role="Receiving specialist",
            state=RequestState.OPEN,
            is_blocking=False,
            due_at=now + timedelta(days=4),
        )
        ProviderResponse.objects.bulk_create(
            [
                ProviderResponse(
                    case=referral,
                    response_type=ResponseType.CLINICAL_OPINION,
                    title="Preliminary specialist response",
                    author_name="Dr. Arun Mehta · synthetic",
                    author_role="Consultant oncologist · fictional profile",
                    organization="Aarunya Cancer Centre · fictional",
                    summary=(
                        "The shared synthetic records have been reviewed. An in-person specialist "
                        "assessment may be appropriate before any treatment decision. The receiving "
                        "team would first confirm the source reports and may request further tests."
                    ),
                    limitations=(
                        "Prototype content only. This is not a diagnosis or treatment recommendation "
                        "and must not be used for a real person's care."
                    ),
                    state=ResponseState.ISSUED,
                    issued_at=now - timedelta(hours=7),
                    version=1,
                ),
                ProviderResponse(
                    case=referral,
                    response_type=ResponseType.COORDINATION_PLAN,
                    title="If the patient chooses to continue",
                    author_name="Aarunya international care team · synthetic",
                    author_role="Hospital coordination",
                    organization="Aarunya Cancer Centre · fictional",
                    summary=(
                        "The next step would be a coordinator call, source-document confirmation, "
                        "and a provisional assessment window. Travel or visa outcomes are not promised."
                    ),
                    limitations="Timing remains indicative until the fictional hospital confirms capacity.",
                    state=ResponseState.ISSUED,
                    issued_at=now - timedelta(hours=6),
                    version=1,
                ),
            ]
        )
        CaseEvent.objects.bulk_create(
            [
                CaseEvent(
                    case=referral,
                    event_type="response_issued",
                    actor_label="Dr. Arun Mehta · synthetic",
                    actor_role="Receiving specialist",
                    summary="Issued a bounded preliminary response for patient and referrer review.",
                    occurred_at=now - timedelta(hours=7),
                ),
                CaseEvent(
                    case=referral,
                    event_type="review_completed",
                    actor_label="Aarunya review team · synthetic",
                    actor_role="Hospital team",
                    summary="Completed the fictional record review and returned an attributable response.",
                    occurred_at=now - timedelta(hours=8),
                ),
                CaseEvent(
                    case=referral,
                    event_type="consent_granted",
                    actor_label="Ama K. · synthetic",
                    actor_role="Patient",
                    summary="Approved the synthetic case-sharing preview for the named receiving team.",
                    occurred_at=now - timedelta(days=2),
                ),
                CaseEvent(
                    case=referral,
                    event_type="referral_created",
                    actor_label="Dr. Lena A. · synthetic",
                    actor_role="Referring doctor",
                    summary="Created the fictional planned-care referral and invited the patient preview.",
                    occurred_at=now - timedelta(days=3),
                ),
            ]
        )
        self.stdout.write(self.style.SUCCESS(f"Seeded synthetic workspace {referral.reference}"))
