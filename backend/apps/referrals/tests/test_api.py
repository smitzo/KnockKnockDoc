import os
from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.identity.models import MembershipRole, MembershipStatus, SecurityAction, SecurityEvent
from apps.referrals.models import (
    AccessScope,
    AssignmentStatus,
    CaseAccessGrant,
    CaseAssignment,
    CaseEvent,
    GrantScope,
    ReferralCase,
)

DEMO_PASSWORD = "Correct-Horse-Referral-Atlas-729!"


class ReferralAuthorizationApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        with patch.dict(os.environ, {"DEMO_ACCOUNT_PASSWORD": DEMO_PASSWORD}):
            call_command("seed_access_demo", verbosity=0)
        cls.referral = ReferralCase.objects.get(reference="KND-DEMO-001")
        user_model = get_user_model()
        cls.patient = user_model.objects.get(username="patient.demo@knocknockdoc.test")
        cls.referrer = user_model.objects.get(username="referrer.demo@knocknockdoc.test")
        cls.specialist = user_model.objects.get(username="specialist.demo@knocknockdoc.test")
        cls.coordinator = user_model.objects.get(username="coordinator.demo@knocknockdoc.test")
        cls.hospital_b = user_model.objects.get(username="hospitalb.demo@knocknockdoc.test")

    def setUp(self):
        cache.clear()
        self.client = APIClient()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def payload(self):
        return {
            "patient_alias": "Patient B · synthetic",
            "patient_country": "Kenya",
            "patient_age_band": "45–59",
            "specialty": "Oncology",
            "clinical_question": (
                "Please review this fictional planned-care referral for specialist fit."
            ),
            "summary": "This is a fully synthetic summary for a product workflow rehearsal only.",
            "is_planned_care": True,
            "accepts_synthetic_only": True,
        }

    def specialist_grant(self):
        assignment = CaseAssignment.objects.get(
            case=self.referral,
            membership__user=self.specialist,
        )
        return CaseAccessGrant.objects.get(assignment=assignment, revoked_at__isnull=True)

    def test_health_remains_anonymous_and_discloses_synthetic_boundary(self):
        response = self.client.get("/api/v1/health/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["prototype_mode"])
        self.assertEqual(response.data["data_policy"], "synthetic-only")
        self.assertEqual(response.headers["X-Prototype-Mode"], "synthetic-only")

    def test_case_endpoints_require_authentication(self):
        self.assertEqual(self.client.get("/api/v1/cases/").status_code, 403)
        self.assertEqual(self.client.get("/api/v1/demo/workspace/").status_code, 403)

    def test_assigned_patient_receives_the_authorized_workspace(self):
        self.authenticate(self.patient)

        response = self.client.get("/api/v1/demo/workspace/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["prototype"]["authorization_enforced"])
        self.assertEqual(response.data["viewer"]["membership_role"], MembershipRole.PATIENT)
        self.assertGreaterEqual(len(response.data["case"]["participants"]), 4)
        self.assertTrue(
            SecurityEvent.objects.filter(
                actor=self.patient,
                action=SecurityAction.CASE_VIEWED,
                target_id=self.referral.id,
            ).exists()
        )

    def test_hospital_b_cannot_discover_hospital_a_case(self):
        self.authenticate(self.hospital_b)

        case_list = self.client.get("/api/v1/cases/")
        detail = self.client.get(f"/api/v1/cases/{self.referral.id}/")
        demo = self.client.get("/api/v1/demo/workspace/")

        self.assertEqual(case_list.status_code, 200)
        self.assertEqual(case_list.data["count"], 0)
        self.assertEqual(detail.status_code, 404)
        self.assertEqual(demo.status_code, 404)

    def test_revoked_grant_denies_case_access(self):
        grant = self.specialist_grant()
        grant.revoked_at = timezone.now()
        grant.revoked_by = self.coordinator
        grant.revocation_reason = "Synthetic access rehearsal ended"
        grant.save()
        self.authenticate(self.specialist)

        response = self.client.get(f"/api/v1/cases/{self.referral.id}/")

        self.assertEqual(response.status_code, 404)

    def test_expired_grant_denies_case_access(self):
        grant = self.specialist_grant()
        grant.granted_at = timezone.now() - timedelta(days=2)
        grant.expires_at = timezone.now() - timedelta(seconds=1)
        grant.save()
        self.authenticate(self.specialist)

        response = self.client.get(f"/api/v1/cases/{self.referral.id}/")

        self.assertEqual(response.status_code, 404)

    def test_ended_assignment_denies_case_access(self):
        assignment = self.specialist_grant().assignment
        assignment.status = AssignmentStatus.ENDED
        assignment.ends_at = timezone.now()
        assignment.save()
        self.authenticate(self.specialist)

        response = self.client.get(f"/api/v1/cases/{self.referral.id}/")

        self.assertEqual(response.status_code, 404)

    def test_suspended_membership_denies_case_access(self):
        membership = self.specialist.organization_memberships.get(role=MembershipRole.SPECIALIST)
        membership.status = MembershipStatus.SUSPENDED
        membership.save()
        self.authenticate(self.specialist)

        response = self.client.get(f"/api/v1/cases/{self.referral.id}/")

        self.assertEqual(response.status_code, 404)

    def test_missing_view_scope_denies_case_access(self):
        GrantScope.objects.filter(
            grant=self.specialist_grant(),
            scope=AccessScope.CASE_VIEW,
        ).delete()
        self.authenticate(self.specialist)

        response = self.client.get(f"/api/v1/cases/{self.referral.id}/")

        self.assertEqual(response.status_code, 404)

    def test_referrer_creates_case_with_server_derived_identity_and_access(self):
        self.authenticate(self.referrer)

        response = self.client.post("/api/v1/cases/", self.payload(), format="json")

        self.assertEqual(response.status_code, 201)
        referral = ReferralCase.objects.get(id=response.data["id"])
        self.assertTrue(referral.is_synthetic)
        self.assertTrue(referral.is_planned_care)
        self.assertEqual(CaseEvent.objects.filter(case=referral).count(), 1)
        referrer_participant = referral.participants.get(role="referrer")
        self.assertEqual(
            referrer_participant.display_name,
            self.referrer.identity_profile.display_name,
        )
        assignment = CaseAssignment.objects.get(case=referral, membership__user=self.referrer)
        self.assertTrue(
            GrantScope.objects.filter(
                grant__assignment=assignment,
                scope=AccessScope.CASE_VIEW,
            ).exists()
        )
        self.assertTrue(
            SecurityEvent.objects.filter(
                actor=self.referrer,
                action=SecurityAction.CASE_CREATED,
                target_id=referral.id,
            ).exists()
        )

    def test_non_referrer_cannot_create_case(self):
        self.authenticate(self.patient)

        response = self.client.post("/api/v1/cases/", self.payload(), format="json")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(ReferralCase.objects.count(), 1)

    def test_mutating_session_request_requires_a_fresh_csrf_token(self):
        client = APIClient(enforce_csrf_checks=True)
        csrf_response = client.get("/api/v1/auth/csrf/")
        login_response = client.post(
            "/api/v1/auth/login/",
            {
                "email": "referrer.demo@knocknockdoc.test",
                "password": DEMO_PASSWORD,
            },
            format="json",
            HTTP_X_CSRFTOKEN=csrf_response.data["csrf_token"],
        )
        self.assertEqual(login_response.status_code, 200)

        missing_csrf = client.post("/api/v1/cases/", self.payload(), format="json")
        fresh_csrf = client.get("/api/v1/auth/csrf/").data["csrf_token"]
        accepted = client.post(
            "/api/v1/cases/",
            self.payload(),
            format="json",
            HTTP_X_CSRFTOKEN=fresh_csrf,
        )

        self.assertEqual(missing_csrf.status_code, 403)
        self.assertEqual(accepted.status_code, 201)

    def test_rejects_emergency_like_scenario_without_storing_it(self):
        self.authenticate(self.referrer)
        payload = self.payload()
        payload["clinical_question"] = (
            "This fictional person cannot breathe and needs a review right now."
        )

        response = self.client.post("/api/v1/cases/", payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "not an emergency", status_code=400)
        self.assertEqual(ReferralCase.objects.count(), 1)

    def test_rejects_contact_details_in_patient_alias(self):
        self.authenticate(self.referrer)
        payload = self.payload()
        payload["patient_alias"] = "patient@example.com"

        response = self.client.post("/api/v1/cases/", payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("patient_alias", response.data)
