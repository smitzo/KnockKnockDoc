from datetime import timedelta

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.demo_lab.bootstrap import (
    DemoCredentialError,
    require_demo_password,
    upsert_synthetic_account,
)
from apps.demo_lab.fixtures import load_product_demo_fixture
from apps.identity.models import (
    MembershipStatus,
    Organization,
    OrganizationMembership,
    OrganizationStatus,
)
from apps.referrals.models import (
    AssignmentStatus,
    CaseAccessGrant,
    CaseAssignment,
    GrantScope,
)
from apps.referrals.selectors import get_demo_workspace


class Command(BaseCommand):
    help = "Load synthetic identities and case grants from the versioned JSON fixture."

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            password = require_demo_password("DEMO_ACCOUNT_PASSWORD")
        except DemoCredentialError as exc:
            raise CommandError(str(exc)) from exc

        fixture = load_product_demo_fixture()
        call_command("seed_demo", verbosity=0)
        now = timezone.now()
        organizations = self._upsert_organizations(fixture.organizations)
        memberships = {}
        try:
            for account in fixture.access_accounts:
                memberships[account["fixture_key"]] = self._upsert_identity(
                    account=account,
                    organization=organizations[account["organization_fixture_key"]],
                    password=password,
                    verified_at=now,
                )
        except DemoCredentialError as exc:
            raise CommandError(str(exc)) from exc

        referral = get_demo_workspace()
        grantor = memberships["coordinator-demo"].user
        expires_at = now + timedelta(days=fixture.referral_workspace["access_expires_days"])
        for grant_spec in fixture.referral_workspace["access_grants"]:
            self._upsert_access(
                referral=referral,
                membership=memberships[grant_spec["account_fixture_key"]],
                grantor=grantor,
                scopes=grant_spec["scopes"],
                expires_at=expires_at,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded authenticated synthetic access for {referral.reference}; "
                "the local password was not printed."
            )
        )

    def _upsert_organizations(self, specs):
        organizations = {}
        for spec in specs:
            organizations[spec["fixture_key"]], _created = Organization.objects.update_or_create(
                slug=spec["slug"],
                defaults={
                    "name": spec["name"],
                    "organization_type": spec["organization_type"],
                    "status": OrganizationStatus.ACTIVE,
                },
            )
        return organizations

    def _upsert_identity(self, *, account, organization, password, verified_at):
        user = upsert_synthetic_account(
            email=account["login_email"],
            display_name=account["display_name"],
            account_type=account["account_type"],
            password=password,
            verified_at=verified_at,
        )
        membership, _created = OrganizationMembership.objects.update_or_create(
            user=user,
            organization=organization,
            role=account["membership_role"],
            defaults={
                "status": MembershipStatus.ACTIVE,
                "starts_at": verified_at,
                "ends_at": None,
            },
        )
        return membership

    def _upsert_access(self, *, referral, membership, grantor, scopes, expires_at):
        assignment, _created = CaseAssignment.objects.update_or_create(
            case=referral,
            membership=membership,
            defaults={
                "purpose": "Participate in the named synthetic referral rehearsal",
                "status": AssignmentStatus.ACTIVE,
                "ends_at": None,
            },
        )
        grant = CaseAccessGrant.objects.filter(
            assignment=assignment,
            revoked_at__isnull=True,
        ).first()
        if grant is None:
            grant = CaseAccessGrant.objects.create(
                assignment=assignment,
                purpose="Access the named synthetic referral for the assigned care role",
                granted_by=grantor,
                expires_at=expires_at,
            )
        else:
            grant.purpose = "Access the named synthetic referral for the assigned care role"
            grant.granted_by = grantor
            grant.expires_at = expires_at
            grant.revoked_at = None
            grant.revoked_by = None
            grant.revocation_reason = ""
            grant.save()
        grant.scopes.exclude(scope__in=scopes).delete()
        for scope in scopes:
            GrantScope.objects.get_or_create(grant=grant, scope=scope)
