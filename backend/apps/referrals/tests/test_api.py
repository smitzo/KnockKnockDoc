from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIClient

from apps.referrals.models import CaseEvent, ReferralCase


class PrototypeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_health_discloses_synthetic_boundary(self):
        response = self.client.get("/api/v1/health/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["prototype_mode"])
        self.assertEqual(response.data["data_policy"], "synthetic-only")
        self.assertEqual(response.headers["X-Prototype-Mode"], "synthetic-only")

    def test_seeded_workspace_returns_five_question_aggregate(self):
        call_command("seed_demo", verbosity=0)

        response = self.client.get("/api/v1/demo/workspace/")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["prototype"]["real_patient_data_allowed"])
        case = response.data["case"]
        self.assertTrue(case["clinical_question"])
        self.assertGreaterEqual(len(case["participants"]), 4)
        self.assertGreaterEqual(len(case["records"]), 4)
        self.assertGreaterEqual(len(case["responses"]), 1)
        self.assertTrue(case["next_action"])

    def test_create_case_is_synthetic_and_has_initial_event(self):
        payload = {
            "patient_alias": "Patient B · synthetic",
            "patient_country": "Kenya",
            "patient_age_band": "45–59",
            "specialty": "Oncology",
            "clinical_question": "Please review this fictional planned-care referral for specialist fit.",
            "summary": "This is a fully synthetic summary for a product workflow rehearsal only.",
            "referrer_display_name": "Dr. Referrer B · synthetic",
            "referrer_country": "Kenya",
            "is_planned_care": True,
            "accepts_synthetic_only": True,
        }

        response = self.client.post("/api/v1/cases/", payload, format="json")

        self.assertEqual(response.status_code, 201)
        referral = ReferralCase.objects.get(id=response.data["id"])
        self.assertTrue(referral.is_synthetic)
        self.assertTrue(referral.is_planned_care)
        self.assertEqual(CaseEvent.objects.filter(case=referral).count(), 1)
        self.assertEqual(referral.participants.count(), 2)

    def test_rejects_emergency_like_scenario_without_storing_it(self):
        payload = {
            "patient_alias": "Patient C · synthetic",
            "patient_country": "Kenya",
            "patient_age_band": "30–44",
            "specialty": "Other",
            "clinical_question": "This fictional person cannot breathe and needs a review right now.",
            "summary": "This synthetic scenario should be rejected before any case record is created.",
            "referrer_display_name": "Dr. Referrer C · synthetic",
            "referrer_country": "Kenya",
            "is_planned_care": True,
            "accepts_synthetic_only": True,
        }

        response = self.client.post("/api/v1/cases/", payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "not an emergency", status_code=400)
        self.assertEqual(ReferralCase.objects.count(), 0)

    def test_rejects_contact_details_in_patient_alias(self):
        payload = {
            "patient_alias": "patient@example.com",
            "patient_country": "Kenya",
            "patient_age_band": "30–44",
            "specialty": "Oncology",
            "clinical_question": "Please review this fictional planned-care scenario for specialist fit.",
            "summary": "This is synthetic content, but the alias resembles a direct contact identifier.",
            "referrer_display_name": "Dr. Referrer · synthetic",
            "referrer_country": "Kenya",
            "is_planned_care": True,
            "accepts_synthetic_only": True,
        }

        response = self.client.post("/api/v1/cases/", payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("patient_alias", response.data)
