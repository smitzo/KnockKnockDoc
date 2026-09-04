from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.demo_lab.permissions import IsPlatformAdmin
from apps.demo_lab.selectors import is_demo_mode_enabled
from apps.identity.models import MembershipRole, OrganizationType, SecurityAction
from apps.identity.permissions import HasActiveIdentity
from apps.identity.selectors import active_memberships_for_user
from apps.identity.services import record_security_event

from ..models import ApplicationStatus, ApplicationType, PartnerApplication
from ..services import (
    ApplicationDemoModeError,
    ApplicationPasswordError,
    ApplicationReviewError,
    review_partner_application,
    submit_partner_application,
)
from .serializers import (
    ApplicationReviewActionSerializer,
    PartnerApplicationReviewListSerializer,
    PartnerApplicationReviewSerializer,
    PartnerApplicationSerializer,
)


@method_decorator(csrf_protect, name="dispatch")
class PartnerApplicationCreateView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "partner_registration"

    def post(self, request):
        if not is_demo_mode_enabled():
            return Response(
                {
                    "detail": (
                        "Demo applications are available only after the administrator "
                        "enables demo data."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )
        serializer = PartnerApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            submit_partner_application(validated_data=dict(serializer.validated_data))
        except ApplicationDemoModeError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)
        except ApplicationPasswordError as exc:
            raise ValidationError({"password": [str(exc)]}) from exc
        return Response(
            {
                "accepted": True,
                "message": (
                    "Application received for prototype review. No professional, hospital, "
                    "directory, or referral access has been granted."
                ),
                "next_step": "A platform reviewer must verify the application before activation.",
            },
            status=status.HTTP_202_ACCEPTED,
        )


class ApplicationReviewPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 50


class ApplicationReviewMixin:
    permission_classes = [HasActiveIdentity, IsPlatformAdmin]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "onboarding_review"

    def get_queryset(self):
        if not is_demo_mode_enabled():
            return PartnerApplication.objects.none()
        queryset = PartnerApplication.objects.select_related(
            "reviewer__identity_profile",
            "activated_organization",
            "doctor_details",
            "hospital_details",
        )
        requested_status = self.request.query_params.get("status", "").strip()
        requested_type = self.request.query_params.get("type", "").strip()
        if requested_status in ApplicationStatus.values:
            queryset = queryset.filter(status=requested_status)
        if requested_type in ApplicationType.values:
            queryset = queryset.filter(application_type=requested_type)
        return queryset

    def audit_read(self, request, *, resource, target_id=None):
        membership = (
            active_memberships_for_user(request.user)
            .filter(
                role=MembershipRole.ADMIN,
                organization__organization_type=OrganizationType.PLATFORM,
            )
            .first()
        )
        record_security_event(
            action=SecurityAction.ONBOARDING_REVIEW_VIEWED,
            actor=request.user,
            organization=membership.organization if membership else None,
            target_type="partner_application" if target_id else "",
            target_id=target_id,
            metadata={"resource": resource},
        )


class ApplicationReviewListView(ApplicationReviewMixin, ListAPIView):
    serializer_class = PartnerApplicationReviewListSerializer
    pagination_class = ApplicationReviewPagination

    def list(self, request, *args, **kwargs):
        self.audit_read(request, resource="application_review_queue")
        return super().list(request, *args, **kwargs)


class ApplicationReviewDetailView(ApplicationReviewMixin, RetrieveAPIView):
    serializer_class = PartnerApplicationReviewSerializer
    lookup_url_kwarg = "application_id"

    def retrieve(self, request, *args, **kwargs):
        application = self.get_object()
        self.audit_read(
            request,
            resource="application_review_detail",
            target_id=application.id,
        )
        return Response(self.get_serializer(application).data)


class ApplicationReviewActionView(ApplicationReviewMixin, APIView):
    throttle_scope = "onboarding_review_mutation"

    def post(self, request, application_id, action):
        normalized_action = action.replace("-", "_")
        serializer = ApplicationReviewActionSerializer(
            data=request.data,
            context={"action": normalized_action},
        )
        serializer.is_valid(raise_exception=True)
        try:
            application = review_partner_application(
                actor=request.user,
                application_id=application_id,
                action=normalized_action,
                reason_code=serializer.validated_data.get("reason_code", ""),
                reviewer_note=serializer.validated_data.get("reviewer_note", ""),
            )
        except ApplicationReviewError as exc:
            response_status = (
                status.HTTP_404_NOT_FOUND
                if str(exc) == "Application not found."
                else status.HTTP_409_CONFLICT
            )
            return Response({"detail": str(exc)}, status=response_status)
        application = PartnerApplication.objects.select_related(
            "reviewer__identity_profile",
            "activated_organization",
            "doctor_details",
            "hospital_details",
        ).get(id=application.id)
        return Response(PartnerApplicationReviewSerializer(application).data)
