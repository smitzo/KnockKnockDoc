from collections.abc import Mapping
from uuid import UUID

from django.contrib.auth import get_user_model

from .models import Organization, SecurityAction, SecurityEvent

SAFE_METADATA_KEYS = frozenset({"authentication_method", "membership_role", "scope"})


def normalize_login_email(value: str) -> str:
    return get_user_model().objects.normalize_email(value.strip()).lower()


def record_security_event(
    *,
    action: SecurityAction,
    actor=None,
    organization: Organization | None = None,
    target_type: str = "",
    target_id: UUID | None = None,
    metadata: Mapping[str, str] | None = None,
) -> SecurityEvent:
    safe_metadata = dict(metadata or {})
    disallowed_keys = set(safe_metadata) - SAFE_METADATA_KEYS
    if disallowed_keys:
        raise ValueError("Security event metadata contains a disallowed key.")
    if any(not isinstance(value, str) or len(value) > 120 for value in safe_metadata.values()):
        raise ValueError("Security event metadata values must be short strings.")

    return SecurityEvent.objects.create(
        actor=actor,
        organization=organization,
        action=action,
        target_type=target_type,
        target_id=target_id,
        safe_metadata=safe_metadata,
    )
