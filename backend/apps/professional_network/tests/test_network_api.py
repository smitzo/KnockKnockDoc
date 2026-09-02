import os
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.management import call_command
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from apps.identity.models import SecurityAction, SecurityEvent
from apps.professional_network.models import (
    ConnectionStatus,
    ProfessionalConnection,
    ProfessionalConversation,
    ProfessionalDirectoryProfile,
    ProfessionalMessage,
    ProfessionalRating,
)


ACCOUNT_PASSWORD = "Correct-Horse-Referral-Atlas-729!"
ADMIN_PASSWORD = "Admin-Console-Only-Atlas-843!"


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class ProfessionalNetworkApiTests(TestCase):
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
        cls.doctor_one = users.get(username="doctor01.demo@knocknockdoc.test")
        cls.doctor_two = users.get(username="doctor02.demo@knocknockdoc.test")
        cls.doctor_three = users.get(username="doctor03.demo@knocknockdoc.test")
        cls.referrer = users.get(username="referrer.demo@knocknockdoc.test")
        cls.patient = users.get(username="patient01.demo@knocknockdoc.test")
        cls.coordinator = users.get(username="coordinator.demo@knocknockdoc.test")

    def setUp(self):
        self.client = APIClient()

    def test_doctor_directory_is_bounded_rated_and_excludes_admin_lab_fields(self):
        self.client.force_authenticate(user=self.referrer)

        response = self.client.get("/api/v1/network/doctors/?q=Oncology")

        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.data["count"], 0)
        card = response.data["results"][0]
        self.assertTrue(card["is_synthetic"])
        self.assertEqual(card["rating_count"], 5)
        self.assertGreaterEqual(card["rating_average"], 3)
        self.assertEqual(
            card["rating_breakdown"]["scope"],
            "synthetic_peer_collaboration_not_clinical_quality",
        )
        self.assertIn("specialty", card)
        self.assertIn("experience_years", card)
        self.assertNotIn("login_email", card)
        self.assertNotIn("response_hours", card)
        self.assertNotIn("availability", card)

    def test_patient_and_non_clinical_operator_cannot_open_directory(self):
        for user in [self.patient, self.coordinator]:
            self.client.force_authenticate(user=user)
            response = self.client.get("/api/v1/network/doctors/")
            self.assertEqual(response.status_code, 403)
            self.assertNotIn("results", response.data)

    def test_connection_pair_is_unique_in_both_directions(self):
        recipient = self.doctor_two.professional_directory_profile
        self.client.force_authenticate(user=self.doctor_one)
        created = self.client.post(
            "/api/v1/network/connections/",
            {
                "recipient_profile_id": str(recipient.id),
                "purpose": "referral_collaboration",
                "note": "Explore a fictional professional referral pathway.",
                "accepts_synthetic_only": True,
            },
            format="json",
        )
        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.data["viewer_relation"], "requester")
        self.assertEqual(
            created.data["peer"]["display_name"],
            self.doctor_two.identity_profile.display_name,
        )

        self.client.force_authenticate(user=self.doctor_two)
        reversed_request = self.client.post(
            "/api/v1/network/connections/",
            {
                "recipient_profile_id": str(self.doctor_one.professional_directory_profile.id),
                "purpose": "professional_introduction",
                "note": "A second fictional request.",
                "accepts_synthetic_only": True,
            },
            format="json",
        )
        self.assertEqual(reversed_request.status_code, 400)
        self.assertEqual(ProfessionalConnection.objects.count(), 1)

    def test_only_recipient_accepts_and_acceptance_creates_one_conversation(self):
        connection = self._create_connection()
        self.client.force_authenticate(user=self.doctor_one)
        wrong_actor = self.client.post(
            f"/api/v1/network/connections/{connection.id}/accept/",
            {},
            format="json",
        )
        self.assertEqual(wrong_actor.status_code, 404)

        self.client.force_authenticate(user=self.doctor_two)
        accepted = self.client.post(
            f"/api/v1/network/connections/{connection.id}/accept/",
            {},
            format="json",
        )
        self.assertEqual(accepted.status_code, 200)
        self.assertEqual(accepted.data["status"], ConnectionStatus.ACCEPTED)
        self.assertEqual(accepted.data["viewer_relation"], "recipient")
        self.assertEqual(
            accepted.data["peer"]["display_name"],
            self.doctor_one.identity_profile.display_name,
        )
        self.assertIsNotNone(accepted.data["conversation_id"])
        self.assertEqual(ProfessionalConversation.objects.count(), 1)

        second_accept = self.client.post(
            f"/api/v1/network/connections/{connection.id}/accept/",
            {},
            format="json",
        )
        self.assertEqual(second_accept.status_code, 400)
        self.assertEqual(ProfessionalConversation.objects.count(), 1)

    def test_chat_requires_acceptance_and_is_isolated_to_participants(self):
        connection = self._create_connection()
        pending_conversation = ProfessionalConversation.objects.create(connection=connection)
        self.client.force_authenticate(user=self.doctor_one)
        pending = self.client.get(
            f"/api/v1/network/conversations/{pending_conversation.id}/messages/"
        )
        self.assertEqual(pending.status_code, 404)

        connection.status = ConnectionStatus.ACCEPTED
        connection.save(update_fields=["status", "updated_at"])
        sent = self.client.post(
            f"/api/v1/network/conversations/{pending_conversation.id}/messages/",
            {
                "body": "Hello, I would like to rehearse a fictional referral collaboration.",
                "accepts_synthetic_only": True,
            },
            format="json",
        )
        self.assertEqual(sent.status_code, 201)
        self.assertTrue(sent.data["is_mine"])

        self.client.force_authenticate(user=self.doctor_three)
        outsider = self.client.get(
            f"/api/v1/network/conversations/{pending_conversation.id}/messages/"
        )
        self.assertEqual(outsider.status_code, 404)

    def test_chat_rejects_direct_identifiers_and_audit_excludes_body(self):
        connection = self._create_connection(status=ConnectionStatus.ACCEPTED)
        conversation = ProfessionalConversation.objects.create(connection=connection)
        self.client.force_authenticate(user=self.doctor_one)

        rejected = self.client.post(
            f"/api/v1/network/conversations/{conversation.id}/messages/",
            {
                "body": "The patient MRN is 123456789 and email is person@example.com",
                "accepts_synthetic_only": True,
            },
            format="json",
        )
        self.assertEqual(rejected.status_code, 400)
        self.assertEqual(ProfessionalMessage.objects.count(), 0)

        body = "Could we discuss a fictional oncology referral workflow?"
        accepted = self.client.post(
            f"/api/v1/network/conversations/{conversation.id}/messages/",
            {"body": body, "accepts_synthetic_only": True},
            format="json",
        )
        self.assertEqual(accepted.status_code, 201)
        event = SecurityEvent.objects.filter(action=SecurityAction.NETWORK_MESSAGE_SENT).latest(
            "occurred_at"
        )
        self.assertNotIn(body, str(event.safe_metadata))

    def test_messages_are_application_append_only(self):
        connection = self._create_connection(status=ConnectionStatus.ACCEPTED)
        conversation = ProfessionalConversation.objects.create(connection=connection)
        message = ProfessionalMessage.objects.create(
            conversation=conversation,
            sender=self.doctor_one,
            body="A fictional immutable professional message.",
        )
        message.body = "Changed"
        with self.assertRaises(DjangoValidationError):
            message.save()
        with self.assertRaises(DjangoValidationError):
            ProfessionalMessage.objects.filter(id=message.id).delete()

    def test_seed_creates_transparent_ratings_without_patient_reviewers(self):
        self.assertEqual(ProfessionalDirectoryProfile.objects.count(), 32)
        self.assertEqual(ProfessionalRating.objects.count(), 160)
        self.assertFalse(
            ProfessionalRating.objects.filter(
                reviewer__identity_profile__account_type="patient"
            ).exists()
        )

    def _create_connection(self, status=ConnectionStatus.PENDING):
        return ProfessionalConnection.objects.create(
            requester=self.doctor_one,
            recipient=self.doctor_two,
            purpose="referral_collaboration",
            note="Fictional professional collaboration.",
            status=status,
        )
