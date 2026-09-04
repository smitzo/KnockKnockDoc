from dataclasses import dataclass

from django.db import IntegrityError, transaction
from django.utils import timezone
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

from apps.demo_lab.selectors import lock_demo_mode_enabled
from apps.identity.models import SecurityAction
from apps.identity.services import record_security_event

from .models import (
    ConnectionStatus,
    ProfessionalConnection,
    ProfessionalConversation,
    ProfessionalDirectoryProfile,
    ProfessionalMessage,
)


@dataclass(frozen=True)
class ConnectionRequestCommand:
    recipient_profile_id: str
    purpose: str
    note: str


@transaction.atomic
def request_connection(*, actor, command: ConnectionRequestCommand):
    if not lock_demo_mode_enabled():
        raise PermissionDenied("Demo data is not enabled.")
    actor_profile = ProfessionalDirectoryProfile.objects.filter(
        user=actor,
        is_discoverable=True,
        is_synthetic=True,
    ).first()
    if actor_profile is None:
        raise PermissionDenied("A discoverable professional profile is required.")
    recipient_profile = ProfessionalDirectoryProfile.objects.select_related("user").filter(
        id=command.recipient_profile_id,
        is_discoverable=True,
        accepts_connections=True,
        is_synthetic=True,
    ).first()
    if recipient_profile is None:
        raise ValidationError({"recipient_profile_id": "This professional is unavailable."})
    if recipient_profile.user_id == actor.id:
        raise ValidationError({"recipient_profile_id": "You cannot connect with yourself."})
    try:
        connection = ProfessionalConnection.objects.create(
            requester=actor,
            recipient=recipient_profile.user,
            purpose=command.purpose,
            note=command.note,
        )
    except IntegrityError as exc:
        raise ValidationError(
            {"recipient_profile_id": "A connection already exists between these professionals."}
        ) from exc
    record_security_event(
        action=SecurityAction.NETWORK_CONNECTION_REQUESTED,
        actor=actor,
        target_type="professional_connection",
        target_id=connection.id,
        metadata={"connection_purpose": connection.purpose},
    )
    return connection


@transaction.atomic
def transition_connection(*, actor, connection_id, action):
    if not lock_demo_mode_enabled():
        raise NotFound("Connection not found.")
    connection = ProfessionalConnection.objects.select_for_update().filter(id=connection_id).first()
    if connection is None:
        raise NotFound("Connection not found.")
    if connection.status != ConnectionStatus.PENDING:
        raise ValidationError({"detail": "This connection is no longer pending."})

    if action in {"accept", "decline"}:
        if connection.recipient_id != actor.id:
            raise NotFound("Connection not found.")
        connection.status = (
            ConnectionStatus.ACCEPTED if action == "accept" else ConnectionStatus.DECLINED
        )
        connection.responded_at = timezone.now()
    elif action == "withdraw":
        if connection.requester_id != actor.id:
            raise NotFound("Connection not found.")
        connection.status = ConnectionStatus.WITHDRAWN
        connection.responded_at = timezone.now()
    else:
        raise ValidationError({"action": "Unsupported connection action."})

    connection.save(update_fields=["status", "responded_at", "updated_at"])
    if connection.status == ConnectionStatus.ACCEPTED:
        ProfessionalConversation.objects.get_or_create(connection=connection)
    record_security_event(
        action=SecurityAction.NETWORK_CONNECTION_RESPONDED,
        actor=actor,
        target_type="professional_connection",
        target_id=connection.id,
        metadata={"transition_result": connection.status},
    )
    return connection


@transaction.atomic
def append_message(*, actor, conversation, body):
    if not lock_demo_mode_enabled():
        raise PermissionDenied("Conversation not found.")
    if actor.id not in {conversation.connection.requester_id, conversation.connection.recipient_id}:
        raise PermissionDenied("Conversation not found.")
    if conversation.connection.status != ConnectionStatus.ACCEPTED:
        raise PermissionDenied("Conversation not found.")
    message = ProfessionalMessage.objects.create(
        conversation=conversation,
        sender=actor,
        body=body,
    )
    ProfessionalConversation.objects.filter(id=conversation.id).update(updated_at=timezone.now())
    record_security_event(
        action=SecurityAction.NETWORK_MESSAGE_SENT,
        actor=actor,
        target_type="professional_message",
        target_id=message.id,
        metadata={"scope": "professional_chat"},
    )
    return message
