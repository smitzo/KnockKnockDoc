from rest_framework.permissions import BasePermission

from apps.identity.models import MembershipRole
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
