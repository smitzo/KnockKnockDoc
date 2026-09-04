from rest_framework.permissions import BasePermission

from .models import IdentityProfile, IdentityStatus, VerificationBasis


class HasActiveIdentity(BasePermission):
    message = "An active verified prototype identity is required."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated or not user.is_active:
            return False
        try:
            profile = user.identity_profile
        except (AttributeError, IdentityProfile.DoesNotExist):
            return False
        return (
            profile.status == IdentityStatus.ACTIVE
            and profile.email_verified_at is not None
            and profile.verification_basis != VerificationBasis.UNVERIFIED
        )
