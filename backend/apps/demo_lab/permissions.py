from rest_framework.permissions import BasePermission

from apps.identity.models import MembershipRole, OrganizationType
from apps.identity.selectors import active_memberships_for_user


class IsPlatformAdmin(BasePermission):
    message = "An active platform administrator membership is required."

    def has_permission(self, request, view):
        return active_memberships_for_user(request.user).filter(
            role=MembershipRole.ADMIN,
            organization__organization_type=OrganizationType.PLATFORM,
        ).exists()
