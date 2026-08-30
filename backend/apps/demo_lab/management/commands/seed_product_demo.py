from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.demo_lab.bootstrap import (
    DemoCredentialError,
    ensure_demo_admin,
    require_demo_password,
    upsert_synthetic_account,
)
from apps.demo_lab.fixtures import DemoFixtureError, load_product_demo_fixture
from apps.demo_lab.models import SyntheticDoctorProfile, SyntheticPatientProfile
from apps.identity.models import MembershipStatus, Organization, OrganizationMembership
from apps.professional_network.models import ProfessionalDirectoryProfile, ProfessionalRating


class Command(BaseCommand):
    help = "Load the authenticated synthetic product lab from versioned JSON fixtures."

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.PROTOTYPE_MODE:
            raise CommandError("The synthetic product lab can run only in prototype mode.")
        try:
            account_password = require_demo_password("DEMO_ACCOUNT_PASSWORD")
            admin_password = require_demo_password("DEMO_ADMIN_PASSWORD")
            if account_password == admin_password:
                raise DemoCredentialError(
                    "The demo administrator and participant passwords must be different."
                )
            fixture = load_product_demo_fixture()
            ensure_demo_admin()
        except (DemoCredentialError, DemoFixtureError) as exc:
            raise CommandError(str(exc)) from exc

        call_command("seed_access_demo", verbosity=0)
        now = timezone.now()
        organizations = {
            item["fixture_key"]: Organization.objects.get(slug=item["slug"])
            for item in fixture.organizations
        }
        profiles = self._upsert_doctors(
            fixture.doctors,
            organizations,
            account_password,
            now,
        )
        profiles.update(
            self._upsert_access_demo_profiles(
                fixture.access_professional_profiles,
                fixture.access_accounts,
            )
        )
        self._upsert_professional_ratings(fixture.professional_ratings, profiles)
        self._upsert_patients(
            fixture.patients,
            organizations,
            account_password,
            now,
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Loaded {len(fixture.doctors)} fictional doctors and "
                f"{len(fixture.patients)} fictional patients from {fixture.fixture_id}; "
                "no password was printed."
            )
        )

    def _upsert_doctors(self, specs, organizations, password, verified_at):
        profiles = {}
        for spec in specs:
            hospital = organizations[spec["organization_fixture_key"]]
            try:
                user = upsert_synthetic_account(
                    email=spec["login_email"],
                    display_name=spec["display_name"],
                    account_type=spec["account_type"],
                    password=password,
                    verified_at=verified_at,
                )
            except DemoCredentialError as exc:
                raise CommandError(str(exc)) from exc
            OrganizationMembership.objects.update_or_create(
                user=user,
                organization=hospital,
                role=spec["membership_role"],
                defaults={
                    "status": MembershipStatus.ACTIVE,
                    "starts_at": verified_at,
                    "ends_at": None,
                },
            )
            SyntheticDoctorProfile.objects.update_or_create(
                fixture_key=spec["fixture_key"],
                defaults={
                    "user": user,
                    "display_name": spec["display_name"],
                    "specialty": spec["specialty"],
                    "city": spec["city"],
                    "hospital_name": spec["hospital_name"],
                    "experience_years": spec["experience_years"],
                    "languages": spec["languages"],
                    "availability": spec["availability"],
                    "response_hours": spec["response_hours"],
                    "credential_state": spec["credential_state"],
                    "avatar_key": spec["avatar_key"],
                    "profile_summary": spec["profile_summary"],
                    "is_synthetic": spec["is_synthetic"],
                },
            )
            profile, _created = ProfessionalDirectoryProfile.objects.update_or_create(
                user=user,
                defaults={
                    "professional_role": spec["professional_role"],
                    "specialty": spec["specialty"],
                    "experience_years": spec["experience_years"],
                    "country": spec["country"],
                    "city": spec["city"],
                    "organization_name": spec["hospital_name"],
                    "languages": spec["languages"],
                    "professional_summary": spec["professional_summary"],
                    "avatar_key": spec["avatar_key"],
                    "is_discoverable": True,
                    "accepts_connections": True,
                    "is_synthetic": spec["is_synthetic"],
                },
            )
            profiles[spec["fixture_key"]] = profile
        return profiles

    def _upsert_access_demo_profiles(self, specs, account_specs):
        account_by_key = {item["fixture_key"]: item for item in account_specs}
        user_model = get_user_model()
        profiles = {}
        for spec in specs:
            account = account_by_key[spec["fixture_key"]]
            user = user_model.objects.get(username=account["login_email"])
            profile, _created = ProfessionalDirectoryProfile.objects.update_or_create(
                user=user,
                defaults={
                    "professional_role": spec["professional_role"],
                    "specialty": spec["specialty"],
                    "experience_years": spec["experience_years"],
                    "country": spec["country"],
                    "city": spec["city"],
                    "organization_name": spec["organization_name"],
                    "languages": spec["languages"],
                    "professional_summary": spec["professional_summary"],
                    "avatar_key": spec["avatar_key"],
                    "is_discoverable": True,
                    "accepts_connections": True,
                    "is_synthetic": spec["is_synthetic"],
                },
            )
            profiles[spec["fixture_key"]] = profile
        return profiles

    def _upsert_professional_ratings(self, specs, profiles):
        ProfessionalRating.objects.filter(is_synthetic=True).delete()
        ProfessionalRating.objects.bulk_create(
            [
                ProfessionalRating(
                    reviewer=profiles[spec["reviewer_profile_fixture_key"]].user,
                    subject=profiles[spec["subject_profile_fixture_key"]],
                    communication_score=spec["communication_score"],
                    collaboration_score=spec["collaboration_score"],
                    handback_score=spec["handback_score"],
                    comment=spec["comment"],
                    is_synthetic=spec["is_synthetic"],
                )
                for spec in specs
            ]
        )

    def _upsert_patients(self, specs, organizations, password, verified_at):
        for spec in specs:
            try:
                user = upsert_synthetic_account(
                    email=spec["login_email"],
                    display_name=spec["display_alias"],
                    account_type=spec["account_type"],
                    password=password,
                    verified_at=verified_at,
                )
            except DemoCredentialError as exc:
                raise CommandError(str(exc)) from exc
            OrganizationMembership.objects.update_or_create(
                user=user,
                organization=organizations[spec["organization_fixture_key"]],
                role=spec["membership_role"],
                defaults={
                    "status": MembershipStatus.ACTIVE,
                    "starts_at": verified_at,
                    "ends_at": None,
                },
            )
            SyntheticPatientProfile.objects.update_or_create(
                fixture_key=spec["fixture_key"],
                defaults={
                    "user": user,
                    "display_alias": spec["display_alias"],
                    "home_country": spec["home_country"],
                    "age_band": spec["age_band"],
                    "specialty_interest": spec["specialty_interest"],
                    "journey_stage": spec["journey_stage"],
                    "preferred_city": spec["preferred_city"],
                    "language": spec["language"],
                    "coordination_need": spec["coordination_need"],
                    "avatar_key": spec["avatar_key"],
                    "is_synthetic": spec["is_synthetic"],
                },
            )
