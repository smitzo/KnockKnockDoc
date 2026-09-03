import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.identity.models import (
    AccountType,
    IdentityProfile,
    IdentityStatus,
    MembershipRole,
    MembershipStatus,
    Organization,
    OrganizationMembership,
    OrganizationStatus,
)
from apps.identity.services import normalize_login_email

from .fixtures import load_product_demo_fixture


class DemoCredentialError(ValueError):
    pass


def require_demo_password(name: str) -> str:
    password = os.environ.get(name, "")
    if (
        name == "DEMO_ADMIN_PASSWORD"
        and password == "admin"
        and settings.ALLOW_INSECURE_LOCAL_DEMO_ADMIN
        and settings.PROTOTYPE_MODE
        and settings.DEBUG
    ):
        return password
    if len(password) < 14:
        raise DemoCredentialError(f"{name} must be set locally to at least 14 characters.")
    if password.lower() in {"admin", "adminadmin", "password", "password123"}:
        raise DemoCredentialError(f"{name} is a known weak password.")
    return password


def upsert_synthetic_account(
    *,
    email: str,
    display_name: str,
    account_type: str,
    password: str,
    verified_at,
    allow_insecure_local_password: bool = False,
):
    normalized_email = normalize_login_email(email)
    user_model = get_user_model()
    user, _created = user_model.objects.get_or_create(
        username=normalized_email,
        defaults={"email": normalized_email, "is_active": True},
    )
    user.email = normalized_email
    user.is_active = True
    if not allow_insecure_local_password:
        try:
            validate_password(password, user=user)
        except ValidationError as exc:
            raise DemoCredentialError(
                "A local demo password does not meet Django validators."
            ) from exc
    if not user.check_password(password):
        user.set_password(password)
    user.save(update_fields=["email", "is_active", "password"])
    IdentityProfile.objects.update_or_create(
        user=user,
        defaults={
            "normalized_email": normalized_email,
            "display_name": display_name,
            "account_type": account_type,
            "status": IdentityStatus.ACTIVE,
            "email_verified_at": verified_at,
        },
    )
    return user


@transaction.atomic
def ensure_demo_admin():
    if not settings.PROTOTYPE_MODE:
        raise DemoCredentialError("The demo administrator can exist only in prototype mode.")
    password = require_demo_password("DEMO_ADMIN_PASSWORD")
    fixture = load_product_demo_fixture()
    platform_spec = next(
        item for item in fixture.organizations if item["fixture_key"] == "platform"
    )
    platform, _created = Organization.objects.update_or_create(
        slug=platform_spec["slug"],
        defaults={
            "name": platform_spec["name"],
            "organization_type": platform_spec["organization_type"],
            "status": OrganizationStatus.ACTIVE,
        },
    )
    now = timezone.now()
    admin_email = normalize_login_email(
        os.environ.get("DEMO_ADMIN_EMAIL", "admin.demo@knocknockdoc.test")
    )
    admin = upsert_synthetic_account(
        email=admin_email,
        display_name="Platform administrator · synthetic",
        account_type=AccountType.COORDINATOR,
        password=password,
        verified_at=now,
        allow_insecure_local_password=(
            settings.ALLOW_INSECURE_LOCAL_DEMO_ADMIN and password == "admin"
        ),
    )
    OrganizationMembership.objects.update_or_create(
        user=admin,
        organization=platform,
        role=MembershipRole.ADMIN,
        defaults={
            "status": MembershipStatus.ACTIVE,
            "starts_at": now,
            "ends_at": None,
        },
    )
    return admin
