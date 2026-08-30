import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.demo_lab.models import (
    DoctorAvailability,
    PatientJourneyStage,
    SyntheticDoctorProfile,
    SyntheticPatientProfile,
)
from apps.identity.models import (
    AccountType,
    IdentityProfile,
    IdentityStatus,
    MembershipRole,
    MembershipStatus,
    Organization,
    OrganizationMembership,
    OrganizationStatus,
    OrganizationType,
)
from apps.identity.services import normalize_login_email
from apps.professional_network.models import (
    ProfessionalDirectoryProfile,
    ProfessionalRating,
    ProfessionalRole,
)


DOCTOR_NAMES = [
    "Dr. Aanya Rao",
    "Dr. Vihaan Sen",
    "Dr. Mira Kapoor",
    "Dr. Arjun Nair",
    "Dr. Kavya Iyer",
    "Dr. Rohan Mehta",
    "Dr. Nisha Bose",
    "Dr. Dev Malhotra",
    "Dr. Tara Menon",
    "Dr. Kabir Shah",
    "Dr. Leela Joshi",
    "Dr. Aditya Batra",
    "Dr. Sana Kulkarni",
    "Dr. Neel Varma",
    "Dr. Isha Reddy",
    "Dr. Aarav Khanna",
    "Dr. Diya Pillai",
    "Dr. Reyansh Gupta",
    "Dr. Anika Desai",
    "Dr. Ishaan Sethi",
    "Dr. Myra Chawla",
    "Dr. Arnav Dutta",
    "Dr. Riya Narang",
    "Dr. Dhruv Bansal",
    "Dr. Siya Krishnan",
    "Dr. Yuvan Chopra",
    "Dr. Veda Anand",
    "Dr. Samar Roy",
    "Dr. Navya Prasad",
    "Dr. Veer Oberoi",
]

SPECIALTIES = [
    "Oncology",
    "Cardiac sciences",
    "Neurology",
    "Orthopaedics",
    "Transplant medicine",
    "Complex surgery",
]
CITY_SPECS = [
    ("Delhi NCR", "Saanvi Institute of Medical Sciences · fictional", "saanvi-delhi"),
    ("Mumbai", "Harbourview Specialist Hospital · fictional", "harbourview-mumbai"),
    ("Bengaluru", "Cedar Grove Medical Centre · fictional", "cedar-bengaluru"),
    ("Chennai", "Marina Advanced Care Institute · fictional", "marina-chennai"),
    ("Hyderabad", "Deccan Clinical Centre · fictional", "deccan-hyderabad"),
    ("Kochi", "Backwater International Hospital · fictional", "backwater-kochi"),
]
PATIENT_COUNTRIES = [
    "Kenya",
    "Tanzania",
    "Nigeria",
    "Bangladesh",
    "Nepal",
    "Oman",
    "Uganda",
    "Ethiopia",
    "Ghana",
    "Sri Lanka",
]
AGE_BANDS = ["18–29", "30–44", "45–59", "60–74", "75+"]
LANGUAGES = ["English", "Swahili", "Bengali", "Arabic", "Nepali", "French"]
COORDINATION_NEEDS = [
    "Clarify the next record needed",
    "Prepare questions for the home doctor",
    "Understand the preliminary response",
    "Compare the plan with personal priorities",
    "Prepare an attributable handback summary",
]


class Command(BaseCommand):
    help = "Seed the authenticated, admin-only synthetic product lab."

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.PROTOTYPE_MODE:
            raise CommandError("The synthetic product lab can run only in prototype mode.")

        account_password = os.environ.get("DEMO_ACCOUNT_PASSWORD", "")
        admin_password = os.environ.get("DEMO_ADMIN_PASSWORD", "")
        if len(account_password) < 14 or len(admin_password) < 14:
            raise CommandError(
                "DEMO_ACCOUNT_PASSWORD and DEMO_ADMIN_PASSWORD must each be at least 14 characters."
            )
        if account_password == admin_password:
            raise CommandError(
                "The demo administrator and participant passwords must be different."
            )

        call_command("seed_access_demo", verbosity=0)
        now = timezone.now()
        platform = Organization.objects.get(slug="knock-knock-doc")
        admin_email = normalize_login_email(
            os.environ.get("DEMO_ADMIN_EMAIL", "admin.demo@knocknockdoc.test")
        )
        admin = self._upsert_account(
            email=admin_email,
            display_name="Platform administrator · synthetic",
            account_type=AccountType.COORDINATOR,
            password=admin_password,
            verified_at=now,
        )
        OrganizationMembership.objects.update_or_create(
            user=admin,
            organization=platform,
            role=MembershipRole.ADMIN,
            defaults={
                "status": MembershipStatus.ACTIVE,
                "starts_at": now,
                "ends_at": None,
            },
        )

        hospitals = self._upsert_hospitals()
        directory_profiles = self._upsert_doctors(hospitals, account_password, now)
        directory_profiles.extend(self._upsert_access_demo_profiles())
        self._upsert_professional_ratings(directory_profiles)
        self._upsert_patients(platform, account_password, now)
        self.stdout.write(
            self.style.SUCCESS(
                "Seeded 30 fictional doctors and 30 fictional patients for the admin-only lab; "
                "no password was printed."
            )
        )

    def _upsert_hospitals(self):
        hospitals = []
        for city, name, slug in CITY_SPECS:
            hospital, _created = Organization.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "organization_type": OrganizationType.HOSPITAL,
                    "status": OrganizationStatus.ACTIVE,
                },
            )
            hospitals.append((city, hospital))
        return hospitals

    def _upsert_doctors(self, hospitals, password, verified_at):
        availability_values = list(DoctorAvailability.values)
        directory_profiles = []
        for index, name in enumerate(DOCTOR_NAMES, start=1):
            city, hospital = hospitals[(index - 1) % len(hospitals)]
            specialty = SPECIALTIES[(index - 1) % len(SPECIALTIES)]
            email = f"doctor{index:02d}.demo@knocknockdoc.test"
            user = self._upsert_account(
                email=email,
                display_name=f"{name} · synthetic",
                account_type=AccountType.PROFESSIONAL,
                password=password,
                verified_at=verified_at,
            )
            OrganizationMembership.objects.update_or_create(
                user=user,
                organization=hospital,
                role=MembershipRole.SPECIALIST,
                defaults={
                    "status": MembershipStatus.ACTIVE,
                    "starts_at": verified_at,
                    "ends_at": None,
                },
            )
            SyntheticDoctorProfile.objects.update_or_create(
                fixture_key=f"doctor-{index:02d}",
                defaults={
                    "user": user,
                    "display_name": f"{name} · synthetic",
                    "specialty": specialty,
                    "city": city,
                    "hospital_name": hospital.name,
                    "experience_years": 7 + ((index * 3) % 24),
                    "languages": ["English", "Hindi", LANGUAGES[index % len(LANGUAGES)]],
                    "availability": availability_values[(index - 1) % 3],
                    "response_hours": 12 + ((index * 7) % 61),
                    "credential_state": "synthetic_verified",
                    "avatar_key": f"doctor-{index:02d}",
                    "profile_summary": (
                        f"Fictional {specialty.lower()} profile for referral-flow rehearsal. "
                        "No real credential or clinical claim is represented."
                    ),
                    "is_synthetic": True,
                },
            )
            directory_profile, _created = ProfessionalDirectoryProfile.objects.update_or_create(
                user=user,
                defaults={
                    "professional_role": ProfessionalRole.SPECIALIST,
                    "specialty": specialty,
                    "experience_years": 7 + ((index * 3) % 24),
                    "country": "India",
                    "city": city,
                    "organization_name": hospital.name,
                    "languages": ["English", "Hindi", LANGUAGES[index % len(LANGUAGES)]],
                    "professional_summary": (
                        f"Fictional {specialty.lower()} specialist profile for doctor-to-doctor "
                        "discovery and referral rehearsal. No clinical outcome is represented."
                    ),
                    "avatar_key": f"doctor-{index:02d}",
                    "is_discoverable": True,
                    "accepts_connections": True,
                    "is_synthetic": True,
                },
            )
            directory_profiles.append(directory_profile)
        return directory_profiles

    def _upsert_access_demo_profiles(self):
        specs = [
            (
                "referrer.demo@knocknockdoc.test",
                ProfessionalRole.REFERRER,
                "General medicine",
                14,
                "Kenya",
                "Nairobi",
                "Nairobi referring practice · fictional",
                ["English", "Swahili"],
                "doctor-31",
            ),
            (
                "specialist.demo@knocknockdoc.test",
                ProfessionalRole.SPECIALIST,
                "Oncology",
                18,
                "India",
                "New Delhi",
                "Aarunya Cancer Centre · fictional",
                ["English", "Hindi"],
                "doctor-32",
            ),
        ]
        profiles = []
        user_model = get_user_model()
        for email, role, specialty, years, country, city, organization, languages, avatar in specs:
            user = user_model.objects.get(username=email)
            profile, _created = ProfessionalDirectoryProfile.objects.update_or_create(
                user=user,
                defaults={
                    "professional_role": role,
                    "specialty": specialty,
                    "experience_years": years,
                    "country": country,
                    "city": city,
                    "organization_name": organization,
                    "languages": languages,
                    "professional_summary": (
                        "Fictional verified professional profile for a doctor-first connection "
                        "and closed-loop referral rehearsal."
                    ),
                    "avatar_key": avatar,
                    "is_discoverable": True,
                    "accepts_connections": True,
                    "is_synthetic": True,
                },
            )
            profiles.append(profile)
        return profiles

    def _upsert_professional_ratings(self, profiles):
        for subject_index, subject in enumerate(profiles):
            reviewers = [
                profiles[(subject_index + offset) % len(profiles)]
                for offset in range(1, 6)
            ]
            for reviewer_index, reviewer in enumerate(reviewers, start=1):
                ProfessionalRating.objects.update_or_create(
                    reviewer=reviewer.user,
                    subject=subject,
                    defaults={
                        "communication_score": 3 + ((subject_index + reviewer_index) % 3),
                        "collaboration_score": 3 + ((subject_index + reviewer_index + 1) % 3),
                        "handback_score": 3 + ((subject_index + reviewer_index + 2) % 3),
                        "comment": (
                            "Fictional peer collaboration signal for prototype comparison; "
                            "not a clinical quality or outcome review."
                        ),
                        "is_synthetic": True,
                    },
                )

    def _upsert_patients(self, platform, password, verified_at):
        stages = list(PatientJourneyStage.values)
        for index in range(1, 31):
            email = f"patient{index:02d}.demo@knocknockdoc.test"
            alias = f"Patient {index:02d} · synthetic"
            user = self._upsert_account(
                email=email,
                display_name=alias,
                account_type=AccountType.PATIENT,
                password=password,
                verified_at=verified_at,
            )
            OrganizationMembership.objects.update_or_create(
                user=user,
                organization=platform,
                role=MembershipRole.PATIENT,
                defaults={
                    "status": MembershipStatus.ACTIVE,
                    "starts_at": verified_at,
                    "ends_at": None,
                },
            )
            SyntheticPatientProfile.objects.update_or_create(
                fixture_key=f"patient-{index:02d}",
                defaults={
                    "user": user,
                    "display_alias": alias,
                    "home_country": PATIENT_COUNTRIES[(index - 1) % len(PATIENT_COUNTRIES)],
                    "age_band": AGE_BANDS[(index - 1) % len(AGE_BANDS)],
                    "specialty_interest": SPECIALTIES[(index + 1) % len(SPECIALTIES)],
                    "journey_stage": stages[(index - 1) % len(stages)],
                    "preferred_city": CITY_SPECS[(index + 2) % len(CITY_SPECS)][0],
                    "language": LANGUAGES[(index - 1) % len(LANGUAGES)],
                    "coordination_need": COORDINATION_NEEDS[
                        (index - 1) % len(COORDINATION_NEEDS)
                    ],
                    "avatar_key": f"patient-{index:02d}",
                    "is_synthetic": True,
                },
            )

    def _upsert_account(
        self,
        *,
        email,
        display_name,
        account_type,
        password,
        verified_at,
    ):
        normalized_email = normalize_login_email(email)
        user_model = get_user_model()
        user, _created = user_model.objects.get_or_create(
            username=normalized_email,
            defaults={"email": normalized_email, "is_active": True},
        )
        user.email = normalized_email
        user.is_active = True
        try:
            validate_password(password, user=user)
        except ValidationError as exc:
            raise CommandError("A demo password does not meet Django validators.") from exc
        if not user.check_password(password):
            user.set_password(password)
        user.save(update_fields=["email", "is_active", "password"])
        IdentityProfile.objects.update_or_create(
            user=user,
            defaults={
                "normalized_email": normalized_email,
                "display_name": display_name,
                "account_type": account_type,
                "status": IdentityStatus.ACTIVE,
                "email_verified_at": verified_at,
            },
        )
        return user
