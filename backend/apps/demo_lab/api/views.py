from django.db.models import Count, Q
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.identity.models import SecurityAction
from apps.identity.permissions import HasActiveIdentity
from apps.identity.selectors import active_memberships_for_user
from apps.identity.services import record_security_event

from ..models import SyntheticDoctorProfile, SyntheticPatientProfile
from ..permissions import IsPlatformAdmin
from .serializers import SyntheticDoctorSerializer, SyntheticPatientSerializer


class AdminLabPagination(PageNumberPagination):
    page_size = 60
    page_size_query_param = "page_size"
    max_page_size = 100


class AdminLabMixin:
    permission_classes = [HasActiveIdentity, IsPlatformAdmin]

    def audit_read(self, request, resource):
        membership = active_memberships_for_user(request.user).filter(role="admin").first()
        record_security_event(
            action=SecurityAction.ADMIN_LAB_VIEWED,
            actor=request.user,
            organization=membership.organization if membership else None,
            metadata={"resource": resource},
        )


class AdminLabSummaryView(AdminLabMixin, APIView):
    def get(self, request):
        self.audit_read(request, "summary")
        return Response(
            {
                "prototype": {
                    "mode": "synthetic-only",
                    "real_people": False,
                    "admin_only": True,
                },
                "counts": {
                    "doctors": SyntheticDoctorProfile.objects.count(),
                    "patients": SyntheticPatientProfile.objects.count(),
                },
                "doctor_specialties": list(
                    SyntheticDoctorProfile.objects.values("specialty")
                    .annotate(count=Count("id"))
                    .order_by("-count", "specialty")
                ),
                "patient_stages": list(
                    SyntheticPatientProfile.objects.values("journey_stage")
                    .annotate(count=Count("id"))
                    .order_by("journey_stage")
                ),
            }
        )


class SyntheticDoctorListView(AdminLabMixin, ListAPIView):
    serializer_class = SyntheticDoctorSerializer
    pagination_class = AdminLabPagination

    def get_queryset(self):
        query = self.request.query_params.get("q", "").strip()[:80]
        queryset = SyntheticDoctorProfile.objects.select_related("user__identity_profile")
        if query:
            queryset = queryset.filter(
                Q(display_name__icontains=query)
                | Q(specialty__icontains=query)
                | Q(city__icontains=query)
                | Q(hospital_name__icontains=query)
            )
        return queryset

    def list(self, request, *args, **kwargs):
        self.audit_read(request, "doctors")
        return super().list(request, *args, **kwargs)


class SyntheticPatientListView(AdminLabMixin, ListAPIView):
    serializer_class = SyntheticPatientSerializer
    pagination_class = AdminLabPagination

    def get_queryset(self):
        query = self.request.query_params.get("q", "").strip()[:80]
        queryset = SyntheticPatientProfile.objects.select_related("user__identity_profile")
        if query:
            queryset = queryset.filter(
                Q(display_alias__icontains=query)
                | Q(home_country__icontains=query)
                | Q(specialty_interest__icontains=query)
                | Q(preferred_city__icontains=query)
            )
        return queryset

    def list(self, request, *args, **kwargs):
        self.audit_read(request, "patients")
        return super().list(request, *args, **kwargs)
