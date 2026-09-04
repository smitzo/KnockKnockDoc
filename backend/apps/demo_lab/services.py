from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import transaction
from django.db.models import Q

from apps.identity.models import IdentityProfile, Organization, OrganizationMembership
from apps.partner_onboarding.models import PartnerApplication
from apps.professional_network.models import (
    ProfessionalConnection,
    ProfessionalConversation,
    ProfessionalDirectoryProfile,
    ProfessionalMessage,
    ProfessionalRating,
)
from apps.referrals.models import (
    CaseAccessGrant,
    CaseAssignment,
    GrantScope,
    ReferralCase,
)

from .fixtures import ProductDemoFixture, load_product_demo_fixture
from .models import (
    ProductMode,
    ProductModeState,
    SyntheticDoctorProfile,
    SyntheticPatientProfile,
)
from .selectors import PRODUCT_MODE_KEY, is_demo_mode_enabled


DELETE_CONFIRMATION = "DELETE SYNTHETIC DEMO DATA"


class DemoFixtureOperationError(RuntimeError):
    pass


def get_demo_fixture_status() -> dict:
    fixture = load_product_demo_fixture()
    user_model = get_user_model()
    participant_emails = fixture.participant_emails
    fixture_user_ids = list(
        user_model.objects.filter(username__in=participant_emails).values_list("id", flat=True)
    )
    profile_ids = list(
        ProfessionalDirectoryProfile.objects.filter(user_id__in=fixture_user_ids).values_list(
            "id", flat=True
        )
    )
    expected = fixture.expected_counts
    actual = {
        "organizations": Organization.objects.filter(
            slug__in=[item["slug"] for item in fixture.organizations]
        ).count(),
        "access_accounts": user_model.objects.filter(
            username__in=[item["login_email"] for item in fixture.access_accounts]
        ).count(),
        "doctors": SyntheticDoctorProfile.objects.filter(
            fixture_key__in=[item["fixture_key"] for item in fixture.doctors]
        ).count(),
        "patients": SyntheticPatientProfile.objects.filter(
            fixture_key__in=[item["fixture_key"] for item in fixture.patients]
        ).count(),
        "access_professional_profiles": ProfessionalDirectoryProfile.objects.filter(
            user__username__in=[
                next(
                    account["login_email"]
                    for account in fixture.access_accounts
                    if account["fixture_key"] == profile["fixture_key"]
                )
                for profile in fixture.access_professional_profiles
            ]
        ).count(),
        "professional_ratings": ProfessionalRating.objects.filter(
            subject_id__in=profile_ids,
            reviewer_id__in=fixture_user_ids,
            is_synthetic=True,
        ).count(),
        "referral_workspaces": ReferralCase.objects.filter(
            reference=fixture.referral_workspace["reference"],
            is_synthetic=True,
        ).count(),
    }
    loaded = actual == expected
    populated = any(
        actual[key]
        for key in [
            "access_accounts",
            "doctors",
            "patients",
            "access_professional_profiles",
            "professional_ratings",
            "referral_workspaces",
        ]
    )
    return {
        "fixture": {
            "id": fixture.fixture_id,
            "schema_version": fixture.schema_version,
            "synthetic_only": True,
            "disclosure": fixture.manifest["disclosure"],
        },
        "state": "loaded" if loaded else "partial" if populated else "empty",
        "loaded": loaded,
        "enabled": is_demo_mode_enabled(),
        "counts": {
            key: {"actual": actual[key], "expected": value}
            for key, value in expected.items()
        },
    }


@transaction.atomic
def load_demo_data(*, actor=None) -> dict:
    _lock_fixture_namespace()
    try:
        call_command("seed_product_demo", verbosity=0)
    except CommandError as exc:
        raise DemoFixtureOperationError(str(exc)) from exc
    status = get_demo_fixture_status()
    if not status["loaded"]:
        raise DemoFixtureOperationError("The demo fixture did not reach its expected loaded state.")
    ProductModeState.objects.update_or_create(
        key=PRODUCT_MODE_KEY,
        defaults={
            "mode": ProductMode.DEMO,
            "fixture_id": status["fixture"]["id"],
            "changed_by": actor,
        },
    )
    return get_demo_fixture_status()


@transaction.atomic
def delete_demo_data(*, actor=None) -> tuple[dict, dict]:
    fixture = load_product_demo_fixture()
    _lock_fixture_namespace()
    ProductModeState.objects.update_or_create(
        key=PRODUCT_MODE_KEY,
        defaults={
            "mode": ProductMode.STANDARD,
            "fixture_id": "",
            "changed_by": actor,
        },
    )
    user_model = get_user_model()
    fixture_users = user_model.objects.filter(username__in=fixture.participant_emails)
    application_queryset = PartnerApplication.objects.filter(is_synthetic=True)
    application_user_ids = list(application_queryset.values_list("user_id", flat=True))
    application_organization_ids = list(
        application_queryset.filter(activated_organization__isnull=False).values_list(
            "activated_organization_id", flat=True
        )
    )
    fixture_user_ids = list(fixture_users.values_list("id", flat=True))
    demo_user_ids = list({*fixture_user_ids, *application_user_ids})

    connection_ids = list(
        ProfessionalConnection.objects.filter(
            Q(requester_id__in=demo_user_ids) | Q(recipient_id__in=demo_user_ids)
        ).values_list("id", flat=True)
    )
    conversation_ids = list(
        ProfessionalConversation.objects.filter(connection_id__in=connection_ids).values_list(
            "id", flat=True
        )
    )
    removed_messages, _details = ProfessionalMessage._base_manager.filter(
        conversation_id__in=conversation_ids
    ).delete()
    removed_conversations, _details = ProfessionalConversation.objects.filter(
        id__in=conversation_ids
    ).delete()
    removed_connections, _details = ProfessionalConnection.objects.filter(
        id__in=connection_ids
    ).delete()

    directory_profiles = ProfessionalDirectoryProfile.objects.filter(
        user_id__in=demo_user_ids
    )
    directory_profile_ids = list(directory_profiles.values_list("id", flat=True))
    removed_ratings, _details = ProfessionalRating.objects.filter(
        Q(reviewer_id__in=demo_user_ids) | Q(subject_id__in=directory_profile_ids)
    ).delete()
    removed_directory_profiles, _details = directory_profiles.delete()
    removed_doctors, _details = SyntheticDoctorProfile.objects.filter(
        fixture_key__in=[item["fixture_key"] for item in fixture.doctors]
    ).delete()
    removed_patients, _details = SyntheticPatientProfile.objects.filter(
        fixture_key__in=[item["fixture_key"] for item in fixture.patients]
    ).delete()

    case_ids = set(
        CaseAssignment.objects.filter(membership__user_id__in=demo_user_ids).values_list(
            "case_id", flat=True
        )
    )
    case_ids.update(
        ReferralCase.objects.filter(
            reference=fixture.referral_workspace["reference"],
            is_synthetic=True,
        ).values_list("id", flat=True)
    )
    assignment_ids = list(
        CaseAssignment.objects.filter(case_id__in=case_ids).values_list("id", flat=True)
    )
    grant_ids = list(
        CaseAccessGrant.objects.filter(assignment_id__in=assignment_ids).values_list(
            "id", flat=True
        )
    )
    GrantScope.objects.filter(grant_id__in=grant_ids).delete()
    CaseAccessGrant.objects.filter(id__in=grant_ids).delete()
    CaseAssignment.objects.filter(id__in=assignment_ids).delete()
    removed_cases, _details = ReferralCase.objects.filter(id__in=case_ids).delete()

    removed_applications, _details = application_queryset.delete()
    OrganizationMembership.objects.filter(user_id__in=demo_user_ids).delete()
    IdentityProfile.objects.filter(user_id__in=demo_user_ids).delete()
    removed_users, _details = user_model.objects.filter(id__in=demo_user_ids).delete()

    removable_organizations = Organization.objects.filter(
        Q(
            slug__in=[
                item["slug"]
                for item in fixture.organizations
                if item["fixture_key"] != "platform"
            ]
        )
        | Q(id__in=application_organization_ids),
        memberships__isnull=True,
    )
    removed_organizations, _details = removable_organizations.delete()
    removed = {
        "messages": removed_messages,
        "conversations": removed_conversations,
        "connections": removed_connections,
        "ratings": removed_ratings,
        "directory_profiles": removed_directory_profiles,
        "doctors": removed_doctors,
        "patients": removed_patients,
        "referral_graph_records": removed_cases,
        "applications": removed_applications,
        "users_and_identity_records": removed_users,
        "organizations": removed_organizations,
    }
    return get_demo_fixture_status(), removed


def _lock_fixture_namespace() -> ProductDemoFixture:
    fixture = load_product_demo_fixture()
    try:
        Organization.objects.select_for_update().get(slug="knock-knock-doc")
    except Organization.DoesNotExist as exc:
        raise DemoFixtureOperationError(
            "The persistent prototype administrator must be bootstrapped before demo data changes."
        ) from exc
    return fixture
