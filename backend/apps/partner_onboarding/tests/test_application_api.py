from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from apps.identity.models import IdentityProfile, SecurityAction, SecurityEvent
from apps.partner_onboarding.models import (
    ApplicationStatus,
    DoctorApplicationDetails,
    HospitalApplicationDetails,
    PartnerApplication,
)


PASSWORD = "Correct-Horse-Onboarding-Atlas-729!"


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class PartnerApplicationApiTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient(enforce_csrf_checks=True)

    def test_doctor_application_creates_only_an_inactive_hashed_applicant(self):
        response = self._post_with_csrf(self._doctor_payload())

        self.assertEqual(response.status_code, 202)
        self.assertEqual(
            set(response.data),
            {"accepted", "message", "next_step"},
        )
        application = PartnerApplication.objects.get()
        self.assertEqual(application.status, ApplicationStatus.SUBMITTED)
        self.assertTrue(application.is_synthetic)
        self.assertEqual(application.application_type, "doctor")
        self.assertTrue(DoctorApplicationDetails.objects.filter(application=application).exists())
        self.assertFalse(HospitalApplicationDetails.objects.exists())
        self.assertFalse(application.user.is_active)
        self.assertTrue(application.user.check_password(PASSWORD))
        self.assertNotEqual(application.user.password, PASSWORD)
        self.assertFalse(IdentityProfile.objects.filter(user=application.user).exists())
        self.assertTrue(
            SecurityEvent.objects.filter(
                action=SecurityAction.ONBOARDING_APPLICATION_SUBMITTED,
                actor=application.user,
            ).exists()
        )

    def test_hospital_application_captures_bounded_private_details(self):
        response = self._post_with_csrf(self._hospital_payload())

        self.assertEqual(response.status_code, 202)
        application = PartnerApplication.objects.get(application_type="hospital")
        details = application.hospital_details
        self.assertEqual(details.bed_count, 240)
        self.assertEqual(details.departments, ["Oncology", "Cardiac sciences"])
        self.assertEqual(details.website_url, "https://aarunya.example")
        self.assertFalse(DoctorApplicationDetails.objects.exists())

    def test_registration_requires_csrf_even_when_anonymous(self):
        response = self.client.post(
            "/api/v1/onboarding/applications/",
            self._doctor_payload(),
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(PartnerApplication.objects.count(), 0)

    def test_real_contact_and_credential_values_are_rejected_in_prototype(self):
        doctor = self._doctor_payload()
        doctor["email"] = "doctor@example.com"
        doctor["details"]["synthetic_registration_number"] = "DMC-123456"
        doctor_response = self._post_with_csrf(doctor)

        hospital = self._hospital_payload()
        hospital["details"]["website_url"] = "https://real-hospital.com"
        hospital_response = self._post_with_csrf(hospital)

        self.assertEqual(doctor_response.status_code, 400)
        self.assertEqual(hospital_response.status_code, 400)
        self.assertEqual(PartnerApplication.objects.count(), 0)

    def test_duplicate_email_returns_same_generic_acceptance_without_a_second_account(self):
        first = self._post_with_csrf(self._doctor_payload())
        second = self._post_with_csrf(self._doctor_payload())

        self.assertEqual(first.status_code, 202)
        self.assertEqual(second.status_code, 202)
        self.assertEqual(first.data, second.data)
        self.assertEqual(PartnerApplication.objects.count(), 1)
        self.assertEqual(
            get_user_model().objects.filter(username="anika.referrer@example.test").count(),
            1,
        )

    def test_pending_applicant_cannot_sign_in(self):
        self._post_with_csrf(self._doctor_payload())
        csrf_response = self.client.get("/api/v1/auth/csrf/")

        login = self.client.post(
            "/api/v1/auth/login/",
            {"email": "anika.referrer@example.test", "password": PASSWORD},
            format="json",
            HTTP_X_CSRFTOKEN=csrf_response.data["csrf_token"],
        )

        self.assertEqual(login.status_code, 400)
        self.assertNotIn("profile", login.data)

    def _post_with_csrf(self, payload):
        csrf_response = self.client.get("/api/v1/auth/csrf/")
        return self.client.post(
            "/api/v1/onboarding/applications/",
            payload,
            format="json",
            HTTP_X_CSRFTOKEN=csrf_response.data["csrf_token"],
        )

    def _doctor_payload(self):
        return {
            "application_type": "doctor",
            "email": "anika.referrer@example.test",
            "password": PASSWORD,
            "legal_name": "Dr. Anika Referrer · fictional",
            "display_name": "Dr. Anika Referrer · fictional",
            "country": "Kenya",
            "city": "Nairobi",
            "timezone": "Africa/Nairobi",
            "preferred_language": "English",
            "organization_name": "Nairobi Referral Practice · fictional",
            "professional_summary": (
                "Fictional referring doctor application for testing the prototype review flow."
            ),
            "terms_version": "prototype-2026-08-11",
            "accepts_synthetic_only": True,
            "details": {
                "professional_role": "referrer",
                "primary_specialty": "General medicine",
                "subspecialties": ["Planned-care referrals"],
                "current_designation": "Consultant · fictional",
                "experience_start_year": 2012,
                "council_jurisdiction": "Synthetic Medical Council",
                "synthetic_registration_number": "SYN-KEN-2048",
                "qualifications": ["MBBS equivalent · fictional"],
                "languages": ["English", "Swahili"],
            },
        }

    def _hospital_payload(self):
        return {
            "application_type": "hospital",
            "email": "partnerships@aarunya.example.test",
            "password": PASSWORD,
            "legal_name": "Aarunya Hospital Private Limited · fictional",
            "display_name": "Aarunya Hospital · fictional",
            "country": "India",
            "city": "New Delhi",
            "timezone": "Asia/Kolkata",
            "preferred_language": "English",
            "organization_name": "Aarunya Hospital · fictional",
            "professional_summary": (
                "Fictional multi-specialty hospital application for prototype review testing."
            ),
            "terms_version": "prototype-2026-08-11",
            "accepts_synthetic_only": True,
            "details": {
                "organization_type": "multi_specialty",
                "representative_title": "Director, International Partnerships · fictional",
                "website_url": "https://aarunya.example",
                "establishment_year": 2008,
                "departments": ["Oncology", "Cardiac sciences"],
                "accreditation_labels": ["Synthetic accreditation rehearsal"],
                "bed_count": 240,
                "capacity_as_of": "2026-08-01",
                "international_patient_services": ["Interpreter coordination"],
                "languages": ["English", "Hindi", "Arabic"],
            },
        }
