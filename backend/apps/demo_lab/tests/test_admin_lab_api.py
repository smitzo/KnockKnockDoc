import os
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management.base import CommandError
from django.core.management import call_command
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from apps.demo_lab.models import SyntheticDoctorProfile, SyntheticPatientProfile
from apps.referrals.models import CaseAssignment

ACCOUNT_PASSWORD = "Correct-Horse-Referral-Atlas-729!"
ADMIN_PASSWORD = "Admin-Console-Only-Atlas-843!"


@override_settings(
    PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
)
class AdminSyntheticLabApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        with patch.dict(
            os.environ,
            {
                "DEMO_ACCOUNT_PASSWORD": ACCOUNT_PASSWORD,
                "DEMO_ADMIN_PASSWORD": ADMIN_PASSWORD,
            },
        ):
            call_command("seed_product_demo", verbosity=0)
        users = get_user_model().objects
        cls.admin = users.get(username="admin.demo@knocknockdoc.test")
        cls.doctor = users.get(username="doctor01.demo@knocknockdoc.test")
        cls.patient = users.get(username="patient01.demo@knocknockdoc.test")
        cls.referrer = users.get(username="referrer.demo@knocknockdoc.test")

    def setUp(self):
        self.client = APIClient()

    def test_seed_creates_bounded_fictional_catalog_and_accounts(self):
        self.assertEqual(SyntheticDoctorProfile.objects.count(), 30)
        self.assertEqual(SyntheticPatientProfile.objects.count(), 30)
        self.assertTrue(self.doctor.has_usable_password())
        self.assertTrue(self.patient.has_usable_password())
        self.assertFalse(
            CaseAssignment.objects.filter(
                membership__user__username__startswith="doctor"
            ).exists()
        )

    def test_platform_admin_can_read_summary_and_all_profiles(self):
        self.client.force_authenticate(user=self.admin)

        summary = self.client.get("/api/v1/admin/lab/summary/")
        doctors = self.client.get("/api/v1/admin/lab/doctors/")
        patients = self.client.get("/api/v1/admin/lab/patients/")

        self.assertEqual(summary.status_code, 200)
        self.assertEqual(summary.data["counts"], {"doctors": 30, "patients": 30})
        self.assertEqual(doctors.status_code, 200)
        self.assertEqual(doctors.data["count"], 30)
        self.assertEqual(len(doctors.data["results"]), 30)
        self.assertEqual(patients.status_code, 200)
        self.assertEqual(patients.data["count"], 30)

    def test_every_non_admin_role_is_denied_without_catalog_rows(self):
        for user in [None, self.patient, self.doctor, self.referrer]:
            self.client.force_authenticate(user=user)
            response = self.client.get("/api/v1/admin/lab/doctors/")
            self.assertIn(response.status_code, {403})
            self.assertNotIn("results", response.data)

    def test_search_is_bounded_and_returns_matching_synthetic_rows(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get("/api/v1/admin/lab/doctors/?q=Oncology")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 5)
        self.assertTrue(all(row["is_synthetic"] for row in response.data["results"]))

    def test_seed_rejects_the_requested_weak_admin_password(self):
        with patch.dict(
            os.environ,
            {
                "DEMO_ACCOUNT_PASSWORD": ACCOUNT_PASSWORD,
                "DEMO_ADMIN_PASSWORD": "admin",
            },
        ):
            with self.assertRaises(CommandError):
                call_command("seed_product_demo", verbosity=0)
