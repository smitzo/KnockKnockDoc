from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from apps.demo_lab.models import ProductMode, ProductModeState
from apps.demo_lab.services import delete_demo_data
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
from apps.partner_onboarding.models import (
    ApplicationStatus,
    DoctorApplicationDetails,
    HospitalApplicationDetails,
    PartnerApplication,
)
from apps.partner_onboarding.services import review_partner_application
from apps.professional_network.models import ProfessionalDirectoryProfile
from apps.referrals.models import CaseAccessGrant, CaseAssignment


PASSWORD = "Correct-Horse-Onboarding-Atlas-729!"


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class PartnerApplicationApiTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient(enforce_csrf_checks=True)
        ProductModeState.objects.create(mode=ProductMode.DEMO, fixture_id="product-demo-v1")

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

    def test_standard_mode_does_not_accept_synthetic_applications(self):
        ProductModeState.objects.filter(key="primary").update(mode=ProductMode.STANDARD)

        response = self._post_with_csrf(self._doctor_payload())

        self.assertEqual(response.status_code, 409)
        self.assertEqual(PartnerApplication.objects.count(), 0)

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


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class PartnerApplicationReviewApiTests(TestCase):
    def setUp(self):
        cache.clear()
        ProductModeState.objects.create(mode=ProductMode.DEMO, fixture_id="product-demo-v1")
        self.platform = Organization.objects.create(
            name="Knock Knock Doc prototype",
            slug="knock-knock-doc",
            organization_type=OrganizationType.PLATFORM,
            status=OrganizationStatus.ACTIVE,
        )
        self.admin = get_user_model().objects.create_user(
            username="reviewer@knocknockdoc.test",
            email="reviewer@knocknockdoc.test",
            password=PASSWORD,
        )
        IdentityProfile.objects.create(
            user=self.admin,
            normalized_email=self.admin.email,
            display_name="Platform reviewer · synthetic",
            account_type=AccountType.COORDINATOR,
            email_verified_at=timezone.now(),
            verification_basis=VerificationBasis.SYNTHETIC_FIXTURE,
        )
        OrganizationMembership.objects.create(
            user=self.admin,
            organization=self.platform,
            role=MembershipRole.ADMIN,
            status=MembershipStatus.ACTIVE,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

    def test_queue_is_admin_only_and_minimizes_list_data(self):
        application = self._create_doctor_application()

        listed = self.client.get("/api/v1/onboarding/review/applications/")
        detail = self.client.get(
            f"/api/v1/onboarding/review/applications/{application.id}/"
        )

        self.assertEqual(listed.status_code, 200)
        row = listed.data["results"][0]
        self.assertNotIn("normalized_email", row)
        self.assertNotIn("legal_name", row)
        self.assertNotIn("details", row)
        self.assertNotIn("reviewer_note", row)
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.data["normalized_email"], application.normalized_email)
        self.assertIn("details", detail.data)

        self.client.force_authenticate(user=application.user)
        denied = self.client.get("/api/v1/onboarding/review/applications/")
        self.assertEqual(denied.status_code, 403)
        self.assertNotIn("results", denied.data)

    def test_doctor_approval_atomically_projects_only_eligible_access(self):
        application = self._create_doctor_application()
        self._start_review(application)

        approved = self.client.post(
            f"/api/v1/onboarding/review/applications/{application.id}/approve/",
            {"reviewer_note": "Private synthetic approval note."},
            format="json",
        )

        self.assertEqual(approved.status_code, 200)
        application.refresh_from_db()
        application.user.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.APPROVED)
        self.assertTrue(application.user.is_active)
        identity = IdentityProfile.objects.get(user=application.user)
        self.assertEqual(identity.verification_basis, VerificationBasis.SYNTHETIC_ADMIN_REVIEW)
        membership = OrganizationMembership.objects.get(user=application.user)
        self.assertEqual(membership.role, MembershipRole.REFERRER)
        self.assertTrue(ProfessionalDirectoryProfile.objects.filter(user=application.user).exists())
        self.assertFalse(CaseAssignment.objects.filter(membership=membership).exists())
        self.assertFalse(
            CaseAccessGrant.objects.filter(assignment__membership=membership).exists()
        )
        event = SecurityEvent.objects.get(
            action=SecurityAction.ONBOARDING_APPLICATION_APPROVED,
            target_id=application.id,
        )
        self.assertNotIn("reviewer_note", event.safe_metadata)
        self.assertNotIn("Private", str(event.safe_metadata))

        browser = APIClient(enforce_csrf_checks=True)
        csrf = browser.get("/api/v1/auth/csrf/")
        login = browser.post(
            "/api/v1/auth/login/",
            {"email": application.normalized_email, "password": PASSWORD},
            format="json",
            HTTP_X_CSRFTOKEN=csrf.data["csrf_token"],
        )
        self.assertEqual(login.status_code, 200)
        self.assertEqual(login.data["profile"]["account_type"], AccountType.PROFESSIONAL)

    def test_hospital_approval_creates_coordinator_without_doctor_card(self):
        application = self._create_hospital_application()
        self._start_review(application)

        approved = self.client.post(
            f"/api/v1/onboarding/review/applications/{application.id}/approve/",
            {},
            format="json",
        )

        self.assertEqual(approved.status_code, 200)
        membership = OrganizationMembership.objects.get(user=application.user)
        self.assertEqual(membership.role, MembershipRole.HOSPITAL_COORDINATOR)
        self.assertEqual(membership.organization.organization_type, OrganizationType.HOSPITAL)
        self.assertFalse(ProfessionalDirectoryProfile.objects.filter(user=application.user).exists())
        self.assertFalse(CaseAssignment.objects.filter(membership=membership).exists())

    def test_invalid_transitions_and_reasonless_changes_are_rejected(self):
        application = self._create_doctor_application()
        premature = self.client.post(
            f"/api/v1/onboarding/review/applications/{application.id}/approve/",
            {},
            format="json",
        )
        self.assertEqual(premature.status_code, 409)
        self._start_review(application)

        missing_reason = self.client.post(
            f"/api/v1/onboarding/review/applications/{application.id}/request-changes/",
            {"reviewer_note": "This private text must not enter the audit event."},
            format="json",
        )
        changed = self.client.post(
            f"/api/v1/onboarding/review/applications/{application.id}/request-changes/",
            {
                "reason_code": "credential_evidence",
                "reviewer_note": "This private text must not enter the audit event.",
            },
            format="json",
        )
        self.assertEqual(missing_reason.status_code, 400)
        self.assertEqual(changed.status_code, 200)
        self.assertEqual(changed.data["status"], ApplicationStatus.CHANGES_REQUESTED)
        event = SecurityEvent.objects.get(
            action=SecurityAction.ONBOARDING_CHANGES_REQUESTED,
            target_id=application.id,
        )
        self.assertEqual(event.safe_metadata["reason_code"], "credential_evidence")
        self.assertNotIn("private", str(event.safe_metadata).lower())

    def test_failed_doctor_projection_rolls_back_every_access_record(self):
        application = self._create_doctor_application()
        self._start_review(application)
        organization_count = Organization.objects.count()

        with patch.object(
            ProfessionalDirectoryProfile.objects,
            "create",
            side_effect=RuntimeError("projection failed"),
        ):
            with self.assertRaises(RuntimeError):
                review_partner_application(
                    actor=self.admin,
                    application_id=application.id,
                    action="approve",
                )

        application.refresh_from_db()
        application.user.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.UNDER_REVIEW)
        self.assertFalse(application.user.is_active)
        self.assertFalse(IdentityProfile.objects.filter(user=application.user).exists())
        self.assertFalse(OrganizationMembership.objects.filter(user=application.user).exists())
        self.assertEqual(Organization.objects.count(), organization_count)

    def test_standard_mode_hides_and_freezes_existing_synthetic_applications(self):
        application = self._create_doctor_application()
        ProductModeState.objects.filter(key="primary").update(mode=ProductMode.STANDARD)

        listed = self.client.get("/api/v1/onboarding/review/applications/")
        detail = self.client.get(
            f"/api/v1/onboarding/review/applications/{application.id}/"
        )
        transition = self.client.post(
            f"/api/v1/onboarding/review/applications/{application.id}/start-review/",
            {},
            format="json",
        )

        self.assertEqual(listed.data["count"], 0)
        self.assertEqual(detail.status_code, 404)
        self.assertEqual(transition.status_code, 409)
        application.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.SUBMITTED)

    def test_demo_delete_removes_review_created_access_but_preserves_admin(self):
        application = self._create_hospital_application()
        self._start_review(application)
        approved = self.client.post(
            f"/api/v1/onboarding/review/applications/{application.id}/approve/",
            {},
            format="json",
        )
        self.assertEqual(approved.status_code, 200)
        user_id = application.user_id
        organization_id = approved.data["activated_organization"]["id"]

        fixture_status, removed = delete_demo_data(actor=self.admin)

        self.assertFalse(fixture_status["enabled"])
        self.assertEqual(fixture_status["state"], "empty")
        self.assertGreaterEqual(removed["applications"], 1)
        self.assertFalse(PartnerApplication.objects.filter(id=application.id).exists())
        self.assertFalse(get_user_model().objects.filter(id=user_id).exists())
        self.assertFalse(Organization.objects.filter(id=organization_id).exists())
        self.assertTrue(get_user_model().objects.filter(id=self.admin.id).exists())

    def _start_review(self, application):
        response = self.client.post(
            f"/api/v1/onboarding/review/applications/{application.id}/start-review/",
            {},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], ApplicationStatus.UNDER_REVIEW)

    def _create_doctor_application(self):
        application = self._create_application(
            application_type="doctor",
            email="review-doctor@example.test",
            display_name="Dr. Review Doctor · fictional",
            organization_name="Review Practice · fictional",
        )
        DoctorApplicationDetails.objects.create(
            application=application,
            professional_role=MembershipRole.REFERRER,
            primary_specialty="General medicine",
            subspecialties=["Planned-care referrals"],
            current_designation="Consultant · fictional",
            experience_start_year=2012,
            council_jurisdiction="Synthetic Medical Council",
            synthetic_registration_number="SYN-REVIEW-1",
            qualifications=["MBBS equivalent · fictional"],
            languages=["English"],
        )
        return application

    def _create_hospital_application(self):
        application = self._create_application(
            application_type="hospital",
            email="review-hospital@example.test",
            display_name="Review Hospital Lead · fictional",
            organization_name="Review Hospital · fictional",
        )
        HospitalApplicationDetails.objects.create(
            application=application,
            organization_type="multi_specialty",
            representative_title="Partnership lead · fictional",
            website_url="https://review-hospital.example",
            establishment_year=2010,
            departments=["Oncology"],
            accreditation_labels=["Synthetic accreditation"],
            bed_count=120,
            capacity_as_of="2026-08-01",
            international_patient_services=["Interpreter coordination"],
            languages=["English"],
        )
        return application

    def _create_application(
        self,
        *,
        application_type,
        email,
        display_name,
        organization_name,
    ):
        user = get_user_model().objects.create_user(
            username=email,
            email=email,
            password=PASSWORD,
            is_active=False,
        )
        return PartnerApplication.objects.create(
            user=user,
            normalized_email=email,
            application_type=application_type,
            legal_name=display_name,
            display_name=display_name,
            country="India" if application_type == "hospital" else "Kenya",
            city="New Delhi" if application_type == "hospital" else "Nairobi",
            timezone="Asia/Kolkata" if application_type == "hospital" else "Africa/Nairobi",
            preferred_language="English",
            organization_name=organization_name,
            professional_summary=(
                "A fully fictional application used to prove the bounded partner review flow."
            ),
            terms_version="prototype-2026-08-11",
            is_synthetic=True,
        )
