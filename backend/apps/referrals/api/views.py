from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import ReferralCase
from ..selectors import get_demo_workspace, referral_workspace_queryset
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

    def get_queryset(self):
        if self.action == "list":
            return ReferralCase.objects.filter(is_synthetic=True).order_by("-updated_at")
        return referral_workspace_queryset().filter(is_synthetic=True)

    def get_serializer_class(self):
        if self.action == "create":
            return ReferralCaseCreateSerializer
        if self.action == "list":
            return ReferralCaseListSerializer
        return ReferralCaseDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), id=kwargs["id"])
        return Response(ReferralCaseDetailSerializer(instance).data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        referral = serializer.save()
        referral = get_object_or_404(referral_workspace_queryset(), id=referral.id)
        return Response(ReferralCaseDetailSerializer(referral).data, status=status.HTTP_201_CREATED)


class DemoWorkspaceView(APIView):
    def get(self, request):
        referral = get_demo_workspace()
        return Response(
            {
                "prototype": {
                    "mode": "synthetic-only",
                    "real_patient_data_allowed": False,
                    "role_switch_is_authorization": False,
                },
                "case": ReferralCaseDetailSerializer(referral).data,
            }
        )
