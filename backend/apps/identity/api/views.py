from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from ..models import IdentityProfile, IdentityStatus, SecurityAction, VerificationBasis
from ..permissions import HasActiveIdentity
from ..selectors import session_payload
from ..services import normalize_login_email, record_security_event
from .serializers import LoginSerializer


class CsrfTokenView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth_csrf"

    def get(self, request):
        return Response({"csrf_token": get_token(request)})


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth_login"

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = normalize_login_email(serializer.validated_data["email"])
        user = authenticate(
            request=request,
            username=email,
            password=serializer.validated_data["password"],
        )
        profile = None
        if user is not None and user.is_active:
            profile = IdentityProfile.objects.filter(
                user=user,
                status=IdentityStatus.ACTIVE,
                email_verified_at__isnull=False,
            ).exclude(verification_basis=VerificationBasis.UNVERIFIED).first()
        if profile is None:
            return Response(
                {"detail": "Email or password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        login(request, user)
        record_security_event(
            action=SecurityAction.LOGIN_SUCCEEDED,
            actor=user,
            target_type="identity_profile",
            target_id=profile.id,
            metadata={"authentication_method": "password_session"},
        )
        return Response(session_payload(user, request.session))


class SessionView(APIView):
    permission_classes = [IsAuthenticated, HasActiveIdentity]

    def get(self, request):
        return Response(session_payload(request.user, request.session))


@method_decorator(csrf_protect, name="dispatch")
class LogoutView(APIView):
    permission_classes = [IsAuthenticated, HasActiveIdentity]

    def post(self, request):
        profile_id = request.user.identity_profile.id
        record_security_event(
            action=SecurityAction.LOGOUT,
            actor=request.user,
            target_type="identity_profile",
            target_id=profile_id,
            metadata={"authentication_method": "password_session"},
        )
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
