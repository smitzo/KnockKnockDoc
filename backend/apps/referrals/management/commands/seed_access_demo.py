import os
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.identity.models import (
    AccountType,
    IdentityProfile,
    MembershipRole,
    MembershipStatus,
    Organization,
    OrganizationMembership,
    OrganizationStatus,
    OrganizationType,
)
from apps.identity.services import normalize_login_email
from apps.referrals.models import (
    AccessScope,
    AssignmentStatus,
    CaseAccessGrant,
    CaseAssignment,
    GrantScope,
)
from apps.referrals.selectors import DEMO_REFERENCE, get_demo_workspace


class Command(BaseCommand):
    help = "Seed synthetic identities and case grants when a local demo password is supplied."

    @transaction.atomic
    def handle(self, *args, **options):
        password = os.environ.get("DEMO_ACCOUNT_PASSWORD", "")
        if len(password) < 14:
            raise CommandError(
                "DEMO_ACCOUNT_PASSWORD must be set locally to at least 14 characters."
            )

        call_command("seed_demo", verbosity=0)
        now = timezone.now()
        organizations = self._upsert_organizations()
        account_specs = [
            (
                "patient.demo@knocknockdoc.test",
                "Ama K. · synthetic",
                AccountType.PATIENT,
                "platform",
                MembershipRole.PATIENT,
            ),
            (
                "referrer.demo@knocknockdoc.test",
                "Dr. Lena A. · synthetic",
                AccountType.PROFESSIONAL,
                "practice",
                MembershipRole.REFERRER,
            ),
            (
                "specialist.demo@knocknockdoc.test",
                "Dr. Arun Mehta · synthetic",
                AccountType.PROFESSIONAL,
                "hospital_a",
                MembershipRole.SPECIALIST,
            ),
            (
                "coordinator.demo@knocknockdoc.test",
                "Nila · prototype coordinator",
                AccountType.COORDINATOR,
                "platform",
                MembershipRole.PLATFORM_COORDINATOR,
            ),
            (
                "hospitalb.demo@knocknockdoc.test",
                "Hospital B coordinator · synthetic",
                AccountType.COORDINATOR,
                "hospital_b",
                MembershipRole.HOSPITAL_COORDINATOR,
            ),
        ]
        memberships = {}
        for email, display_name, account_type, organization_key, role in account_specs:
            memberships[role] = self._upsert_identity(
                email=email,
                display_name=display_name,
                account_type=account_type,
                organization=organizations[organization_key],
                role=role,
                password=password,
                verified_at=now,
            )

        referral = get_demo_workspace()
        grantor = memberships[MembershipRole.PLATFORM_COORDINATOR].user
        access_specs = {
            MembershipRole.PATIENT: [AccessScope.CASE_VIEW],
            MembershipRole.REFERRER: [
                AccessScope.CASE_VIEW,
                AccessScope.CASE_EDIT,
                AccessScope.CASE_MANAGE,
            ],
            MembershipRole.SPECIALIST: [
                AccessScope.CASE_VIEW,
                AccessScope.RECORDS_VIEW,
                AccessScope.RESPONSE_ISSUE,
            ],
            MembershipRole.PLATFORM_COORDINATOR: [
                AccessScope.CASE_VIEW,
                AccessScope.CASE_MANAGE,
            ],
        }
        for role, scopes in access_specs.items():
            self._upsert_access(
                referral=referral,
                membership=memberships[role],
                grantor=grantor,
                scopes=scopes,
                expires_at=now + timedelta(days=90),
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded authenticated synthetic access for {DEMO_REFERENCE}; "
                "the local password was not printed."
            )
        )

    def _upsert_organizations(self):
        specs = {
            "platform": ("Knock Knock Doc prototype", "knock-knock-doc", OrganizationType.PLATFORM),
            "practice": (
                "Nairobi referring practice · fictional",
                "nairobi-referring-practice",
                OrganizationType.REFERRING_PRACTICE,
            ),
            "hospital_a": (
                "Aarunya Cancer Centre · fictional",
                "aarunya-cancer-centre",
                OrganizationType.HOSPITAL,
            ),
            "hospital_b": (
                "Riverview Hospital · fictional",
                "riverview-hospital",
                OrganizationType.HOSPITAL,
            ),
        }
        organizations = {}
        for key, (name, slug, organization_type) in specs.items():
            organizations[key], _created = Organization.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "organization_type": organization_type,
                    "status": OrganizationStatus.ACTIVE,
                },
            )
        return organizations

    def _upsert_identity(
        self,
        *,
        email,
        display_name,
        account_type,
        organization,
        role,
        password,
        verified_at,
    ):
        normalized_email = normalize_login_email(email)
        user_model = get_user_model()
        user, _created = user_model.objects.get_or_create(
            username=normalized_email,
            defaults={"email": normalized_email, "is_active": True},
        )
        user.email = normalized_email
        user.is_active = True
        try:
            validate_password(password, user=user)
        except ValidationError as exc:
            raise CommandError("DEMO_ACCOUNT_PASSWORD does not meet Django validators.") from exc
        user.set_password(password)
        user.save(update_fields=["email", "is_active", "password"])
        IdentityProfile.objects.update_or_create(
            user=user,
            defaults={
                "normalized_email": normalized_email,
                "display_name": display_name,
                "account_type": account_type,
                "status": "active",
                "email_verified_at": verified_at,
            },
        )
        membership, _created = OrganizationMembership.objects.update_or_create(
            user=user,
            organization=organization,
            role=role,
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
