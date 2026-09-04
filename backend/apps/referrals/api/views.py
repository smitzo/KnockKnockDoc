from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.demo_lab.selectors import is_demo_mode_enabled
from apps.identity.models import SecurityAction
from apps.identity.permissions import HasActiveIdentity
from apps.identity.services import record_security_event

from ..models import AccessScope
from ..selectors import (
    active_referrer_memberships,
    authorized_membership_for_case,
    authorized_referral_workspace_queryset,
)
from .serializers import (
    ReferralCaseCreateSerializer,
    ReferralCaseDetailSerializer,
    ReferralCaseListSerializer,
)


class ReferralCaseViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    lookup_field = "id"
    permission_classes = [IsAuthenticated, HasActiveIdentity]

    def get_queryset(self):
        if not is_demo_mode_enabled():
            return authorized_referral_workspace_queryset(self.request.user).none()
        return authorized_referral_workspace_queryset(self.request.user).filter(is_synthetic=True)

    def get_serializer_class(self):
        if self.action == "create":
            return ReferralCaseCreateSerializer
        if self.action == "list":
            return ReferralCaseListSerializer
        return ReferralCaseDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), id=kwargs["id"])
        membership = authorized_membership_for_case(request.user, instance)
        record_security_event(
            action=SecurityAction.CASE_VIEWED,
            actor=request.user,
            organization=membership.organization if membership else None,
            target_type="referral_case",
            target_id=instance.id,
            metadata={"scope": AccessScope.CASE_VIEW},
        )
        return Response(ReferralCaseDetailSerializer(instance).data)

    def create(self, request, *args, **kwargs):
        if not is_demo_mode_enabled():
            raise PermissionDenied("Demo data is not enabled.")
        memberships = list(active_referrer_memberships(request.user)[:2])
        if not memberships:
            raise PermissionDenied("An active verified referrer membership is required.")
        if len(memberships) > 1:
            raise ValidationError(
                {"detail": "Choose a referring organization before creating a referral."}
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        referral = serializer.save(referrer_membership=memberships[0])
        referral = get_object_or_404(self.get_queryset(), id=referral.id)
        return Response(ReferralCaseDetailSerializer(referral).data, status=status.HTTP_201_CREATED)


class DemoWorkspaceView(APIView):
    permission_classes = [IsAuthenticated, HasActiveIdentity]

    def get(self, request):
        if not is_demo_mode_enabled():
            raise PermissionDenied("Demo data is not enabled.")
        referral = get_object_or_404(
            authorized_referral_workspace_queryset(request.user),
            reference="KND-DEMO-001",
            is_synthetic=True,
        )
        membership = authorized_membership_for_case(request.user, referral)
        record_security_event(
            action=SecurityAction.CASE_VIEWED,
            actor=request.user,
            organization=membership.organization if membership else None,
            target_type="referral_case",
            target_id=referral.id,
            metadata={"scope": AccessScope.CASE_VIEW},
        )
        return Response(
            {
                "prototype": {
                    "mode": "synthetic-only",
                    "real_patient_data_allowed": False,
                    "authorization_enforced": True,
                },
                "viewer": {
                    "display_name": request.user.identity_profile.display_name,
                    "membership_role": membership.role,
                    "membership_role_label": membership.get_role_display(),
                    "organization_name": membership.organization.name,
                },
                "case": ReferralCaseDetailSerializer(referral).data,
            }
        )
