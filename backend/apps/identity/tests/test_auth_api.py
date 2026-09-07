from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.identity.models import (
    AccountType,
    IdentityProfile,
    MembershipRole,
    MembershipStatus,
    Organization,
    OrganizationMembership,
    OrganizationStatus,
    OrganizationType,
    SecurityAction,
    SecurityEvent,
    VerificationBasis,
)

DEMO_PASSWORD = "local-test-password-only-42"


class SessionAuthenticationApiTests(TestCase):
    def setUp(self):
        cache.clear()
        self.email = "referrer.test@knocknockdoc.test"
        self.user = get_user_model().objects.create_user(
            username=self.email,
            email=self.email,
            password=DEMO_PASSWORD,
        )
        self.profile = IdentityProfile.objects.create(
            user=self.user,
            normalized_email=self.email,
            display_name="Dr. Referrer · synthetic",
            account_type=AccountType.PROFESSIONAL,
            email_verified_at=timezone.now(),
            verification_basis=VerificationBasis.SYNTHETIC_FIXTURE,
        )
        organization = Organization.objects.create(
            name="Synthetic referring practice",
            slug="synthetic-referring-practice",
            organization_type=OrganizationType.REFERRING_PRACTICE,
            status=OrganizationStatus.ACTIVE,
        )
        self.membership = OrganizationMembership.objects.create(
            user=self.user,
            organization=organization,
            role=MembershipRole.REFERRER,
            status=MembershipStatus.ACTIVE,
        )
        self.client = APIClient(enforce_csrf_checks=True)

    def csrf_token(self):
        response = self.client.get("/api/v1/auth/csrf/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("knd_csrftoken", response.cookies)
        return response.data["csrf_token"]

    def test_login_requires_csrf_and_returns_active_membership(self):
        rejected = self.client.post(
            "/api/v1/auth/login/",
            {"email": self.email, "password": DEMO_PASSWORD},
            format="json",
        )
        self.assertEqual(rejected.status_code, 403)

        response = self.client.post(
            "/api/v1/auth/login/",
            {"email": self.email.upper(), "password": DEMO_PASSWORD},
            format="json",
            HTTP_X_CSRFTOKEN=self.csrf_token(),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["authenticated"])
        self.assertEqual(response.data["profile"]["email"], self.email)
        self.assertEqual(response.data["memberships"][0]["role"], MembershipRole.REFERRER)
        self.assertIn("knd_sessionid", response.cookies)
        self.assertTrue(
            SecurityEvent.objects.filter(
                actor=self.user,
                action=SecurityAction.LOGIN_SUCCEEDED,
            ).exists()
        )

    def test_login_failure_is_enumeration_safe(self):
        token = self.csrf_token()
        wrong_password = self.client.post(
            "/api/v1/auth/login/",
            {"email": self.email, "password": "wrong-password"},
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )
        unknown_email = self.client.post(
            "/api/v1/auth/login/",
            {"email": "unknown@knocknockdoc.test", "password": "wrong-password"},
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(wrong_password.status_code, 400)
        self.assertEqual(unknown_email.status_code, 400)
        self.assertEqual(wrong_password.data, unknown_email.data)

    def test_session_and_logout_require_a_valid_session(self):
        self.assertEqual(self.client.get("/api/v1/auth/session/").status_code, 403)
        token = self.csrf_token()
        self.client.post(
            "/api/v1/auth/login/",
            {"email": self.email, "password": DEMO_PASSWORD},
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(self.client.get("/api/v1/auth/session/").status_code, 200)
        token = self.csrf_token()
        logout_response = self.client.post(
            "/api/v1/auth/logout/",
            {},
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(logout_response.status_code, 204)
        self.assertEqual(self.client.get("/api/v1/auth/session/").status_code, 403)
        self.assertTrue(
            SecurityEvent.objects.filter(actor=self.user, action=SecurityAction.LOGOUT).exists()
        )

    def test_suspended_profile_cannot_log_in(self):
        self.profile.status = "suspended"
        self.profile.save(update_fields=["status", "updated_at"])

        response = self.client.post(
            "/api/v1/auth/login/",
            {"email": self.email, "password": DEMO_PASSWORD},
            format="json",
            HTTP_X_CSRFTOKEN=self.csrf_token(),
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"detail": "Email or password is incorrect."})

    def test_unverified_basis_cannot_authorize_a_session(self):
        self.profile.verification_basis = VerificationBasis.UNVERIFIED
        self.profile.save(update_fields=["verification_basis", "updated_at"])

        response = self.client.post(
            "/api/v1/auth/login/",
            {"email": self.email, "password": DEMO_PASSWORD},
            format="json",
            HTTP_X_CSRFTOKEN=self.csrf_token(),
        )

        self.assertEqual(response.status_code, 400)
        self.assertNotIn("memberships", response.data)
        self.assertEqual(self.client.get("/api/v1/auth/session/").status_code, 403)

    def test_security_events_are_append_only(self):
        event = SecurityEvent.objects.create(
            actor=self.user,
            action=SecurityAction.LOGIN_SUCCEEDED,
            target_type="identity_profile",
            target_id=self.profile.id,
        )
        event.action = SecurityAction.LOGOUT

        with self.assertRaises(ValidationError):
            event.save()
        with self.assertRaises(ValidationError):
            event.delete()
        with self.assertRaises(ValidationError):
            SecurityEvent.objects.filter(id=event.id).update(action=SecurityAction.LOGOUT)
        with self.assertRaises(ValidationError):
            SecurityEvent.objects.filter(id=event.id).delete()
