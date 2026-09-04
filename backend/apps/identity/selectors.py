from django.db.models import Q, QuerySet
from django.utils import timezone

from .models import (
    IdentityStatus,
    MembershipStatus,
    OrganizationMembership,
    OrganizationStatus,
    VerificationBasis,
)


def active_memberships_for_user(user) -> QuerySet[OrganizationMembership]:
    if not user or not user.is_authenticated or not user.is_active:
        return OrganizationMembership.objects.none()

    now = timezone.now()
    return OrganizationMembership.objects.select_related(
        "organization",
        "user__identity_profile",
    ).filter(
        user=user,
        status=MembershipStatus.ACTIVE,
        organization__status=OrganizationStatus.ACTIVE,
        starts_at__lte=now,
        user__identity_profile__status=IdentityStatus.ACTIVE,
        user__identity_profile__email_verified_at__isnull=False,
        user__identity_profile__verification_basis__in=[
            VerificationBasis.SYNTHETIC_FIXTURE,
            VerificationBasis.SYNTHETIC_ADMIN_REVIEW,
            VerificationBasis.EMAIL_TOKEN,
        ],
    ).filter(Q(ends_at__isnull=True) | Q(ends_at__gt=now))


def session_payload(user, session) -> dict:
    profile = user.identity_profile
    memberships = active_memberships_for_user(user)
    return {
        "authenticated": True,
        "profile": {
            "id": str(profile.id),
            "email": profile.normalized_email,
            "display_name": profile.display_name,
            "account_type": profile.account_type,
            "account_type_label": profile.get_account_type_display(),
        },
        "memberships": [
            {
                "id": str(membership.id),
                "role": membership.role,
                "role_label": membership.get_role_display(),
                "organization": {
                    "id": str(membership.organization_id),
                    "name": membership.organization.name,
                    "slug": membership.organization.slug,
                    "type": membership.organization.organization_type,
                },
            }
            for membership in memberships
        ],
        "session": {"expires_at": session.get_expiry_date().isoformat()},
    }
