import os
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management.base import CommandError
from django.core.management import call_command
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from apps.demo_lab.models import (
    ProductMode,
    ProductModeState,
    SyntheticDoctorProfile,
    SyntheticPatientProfile,
)
from apps.demo_lab.fixtures import load_product_demo_fixture
from apps.identity.models import SecurityAction, SecurityEvent
from apps.professional_network.models import (
    ConnectionStatus,
    ProfessionalConnection,
    ProfessionalConversation,
    ProfessionalDirectoryProfile,
    ProfessionalMessage,
    ProfessionalRating,
)
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
        ProductModeState.objects.create(mode=ProductMode.DEMO, fixture_id="product-demo-v1")

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
        self.assertEqual(summary.data["coverage"]["hospitals"], 8)
        self.assertEqual(len(summary.data["hospitals"]), 8)
        self.assertTrue(
            all(hospital["name"].endswith("· fictional") for hospital in summary.data["hospitals"])
        )
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

    @override_settings(
        ALLOW_INSECURE_LOCAL_DEMO_ADMIN=True,
        PROTOTYPE_MODE=True,
        DEBUG=True,
    )
    def test_explicit_local_only_mode_allows_admin_password(self):
        with patch.dict(
            os.environ,
            {
                "DEMO_ACCOUNT_PASSWORD": ACCOUNT_PASSWORD,
                "DEMO_ADMIN_PASSWORD": "admin",
            },
        ):
            call_command("ensure_demo_admin", verbosity=0)

        admin = get_user_model().objects.get(
            username="admin.demo@knocknockdoc.test"
        )
        self.assertTrue(admin.check_password("admin"))

    def test_non_admins_cannot_load_or_delete_fixture_data(self):
        initial_doctors = SyntheticDoctorProfile.objects.count()
        for user in [None, self.patient, self.doctor, self.referrer]:
            self.client.force_authenticate(user=user)
            loaded = self.client.post("/api/v1/admin/lab/fixtures/", {}, format="json")
            deleted = self.client.delete(
                "/api/v1/admin/lab/fixtures/",
                {"confirmation": "DELETE SYNTHETIC DEMO DATA"},
                format="json",
            )
            self.assertEqual(loaded.status_code, 403)
            self.assertEqual(deleted.status_code, 403)
        self.assertEqual(SyntheticDoctorProfile.objects.count(), initial_doctors)


@override_settings(
    PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
)
class AdminDemoFixtureLifecycleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        with patch.dict(os.environ, {"DEMO_ADMIN_PASSWORD": ADMIN_PASSWORD}):
            call_command("ensure_demo_admin", verbosity=0)
        cls.admin = get_user_model().objects.get(
            username="admin.demo@knocknockdoc.test"
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

    def test_fixture_collection_is_versioned_complete_and_has_no_secret_keys(self):
        fixture = load_product_demo_fixture()

        self.assertEqual(fixture.fixture_id, "product-demo-v1")
        self.assertEqual(len(fixture.doctors), 30)
        self.assertEqual(len(fixture.patients), 30)
        self.assertEqual(len(fixture.professional_ratings), 160)
        self.assertFalse(
            any(
                forbidden in item
                for item in [*fixture.access_accounts, *fixture.doctors, *fixture.patients]
                for forbidden in ["password", "secret", "token", "api_key"]
            )
        )

    def test_admin_fixture_mutation_requires_csrf_for_a_browser_session(self):
        browser = APIClient(enforce_csrf_checks=True)
        browser.force_login(self.admin)

        response = browser.post("/api/v1/admin/lab/fixtures/", {}, format="json")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(SyntheticDoctorProfile.objects.count(), 0)

    def test_admin_can_load_delete_and_reload_complete_fixture(self):
        empty = self.client.get("/api/v1/admin/lab/fixtures/")
        self.assertEqual(empty.status_code, 200)
        self.assertEqual(empty.data["state"], "empty")
        self.assertFalse(empty.data["loaded"])
        self.assertFalse(empty.data["enabled"])
        mode = self.client.get("/api/v1/product-mode/")
        self.assertEqual(mode.data, {"mode": "standard", "demo_data_enabled": False})

        first_load = self._load()
        self.assertEqual(first_load.status_code, 200)
        self.assertTrue(first_load.data["loaded"])
        self.assertTrue(first_load.data["enabled"])
        self.assertEqual(SyntheticDoctorProfile.objects.count(), 30)
        self.assertEqual(SyntheticPatientProfile.objects.count(), 30)
        self.assertEqual(ProfessionalDirectoryProfile.objects.count(), 32)
        self.assertEqual(ProfessionalRating.objects.count(), 160)

        second_load = self._load()
        self.assertEqual(second_load.status_code, 200)
        self.assertEqual(SyntheticDoctorProfile.objects.count(), 30)
        self.assertEqual(SyntheticPatientProfile.objects.count(), 30)
        self.assertEqual(ProfessionalRating.objects.count(), 160)

        self._create_demo_conversation()
        rejected = self.client.delete(
            "/api/v1/admin/lab/fixtures/",
            {"confirmation": "delete demo data"},
            format="json",
        )
        self.assertEqual(rejected.status_code, 400)
        self.assertEqual(SyntheticDoctorProfile.objects.count(), 30)

        deleted = self.client.delete(
            "/api/v1/admin/lab/fixtures/",
            {"confirmation": "DELETE SYNTHETIC DEMO DATA"},
            format="json",
        )
        self.assertEqual(deleted.status_code, 200)
        self.assertEqual(deleted.data["fixture_status"]["state"], "empty")
        self.assertFalse(deleted.data["fixture_status"]["enabled"])
        self.assertEqual(SyntheticDoctorProfile.objects.count(), 0)
        self.assertEqual(SyntheticPatientProfile.objects.count(), 0)
        self.assertEqual(ProfessionalDirectoryProfile.objects.count(), 0)
        self.assertEqual(ProfessionalRating.objects.count(), 0)
        self.assertEqual(ProfessionalMessage._base_manager.count(), 0)
        self.assertTrue(get_user_model().objects.filter(id=self.admin.id).exists())
        self.assertFalse(
            get_user_model().objects.filter(username__startswith="doctor01.demo").exists()
        )

        reloaded = self._load()
        self.assertEqual(reloaded.status_code, 200)
        self.assertTrue(reloaded.data["loaded"])
        self.assertTrue(reloaded.data["enabled"])
        self.assertEqual(SyntheticDoctorProfile.objects.count(), 30)
        self.assertTrue(
            SecurityEvent.objects.filter(
                action=SecurityAction.ADMIN_LAB_DELETED,
                actor=self.admin,
            ).exists()
        )

    def test_seeded_rows_stay_hidden_until_demo_mode_is_enabled(self):
        with patch.dict(
            os.environ,
            {
                "DEMO_ACCOUNT_PASSWORD": ACCOUNT_PASSWORD,
                "DEMO_ADMIN_PASSWORD": ADMIN_PASSWORD,
            },
        ):
            call_command("seed_product_demo", verbosity=0)

        summary = self.client.get("/api/v1/admin/lab/summary/")
        doctors = self.client.get("/api/v1/admin/lab/doctors/")

        self.assertEqual(SyntheticDoctorProfile.objects.count(), 30)
        self.assertEqual(summary.data["counts"], {"doctors": 0, "patients": 0})
        self.assertEqual(doctors.data["count"], 0)
        self.assertEqual(
            self.client.get("/api/v1/product-mode/").data,
            {"mode": "standard", "demo_data_enabled": False},
        )

    def _load(self):
        with patch.dict(
            os.environ,
            {
                "DEMO_ACCOUNT_PASSWORD": ACCOUNT_PASSWORD,
                "DEMO_ADMIN_PASSWORD": ADMIN_PASSWORD,
            },
        ):
            return self.client.post("/api/v1/admin/lab/fixtures/", {}, format="json")

    def _create_demo_conversation(self):
        users = get_user_model().objects
        doctor_one = users.get(username="doctor01.demo@knocknockdoc.test")
        doctor_two = users.get(username="doctor02.demo@knocknockdoc.test")
        connection = ProfessionalConnection.objects.create(
            requester=doctor_one,
            recipient=doctor_two,
            purpose="referral_collaboration",
            status=ConnectionStatus.ACCEPTED,
        )
        conversation = ProfessionalConversation.objects.create(connection=connection)
        ProfessionalMessage.objects.create(
            conversation=conversation,
            sender=doctor_one,
            body="Fictional professional workflow rehearsal.",
        )
