from rest_framework.permissions import BasePermission

from apps.identity.models import MembershipRole, OrganizationType
from apps.identity.selectors import active_memberships_for_user


ELIGIBLE_NETWORK_ROLES = {
    MembershipRole.REFERRER,
    MembershipRole.SPECIALIST,
}


class IsVerifiedProfessional(BasePermission):
    message = "An active verified professional membership is required."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        profile = getattr(request.user, "identity_profile", None)
        if profile is None or not profile.is_access_eligible:
            return False
        return active_memberships_for_user(request.user).filter(
            role__in=ELIGIBLE_NETWORK_ROLES
        ).exists()


class IsVerifiedProfessionalOrPlatformAdmin(IsVerifiedProfessional):
    message = "An active professional or platform administrator membership is required."

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return True
        return active_memberships_for_user(request.user).filter(
            role=MembershipRole.ADMIN,
            organization__organization_type=OrganizationType.PLATFORM,
        ).exists()
