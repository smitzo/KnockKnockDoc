from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.demo_lab.selectors import is_demo_mode_enabled

from ..services import (
    ApplicationDemoModeError,
    ApplicationPasswordError,
    submit_partner_application,
)
from .serializers import PartnerApplicationSerializer


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
