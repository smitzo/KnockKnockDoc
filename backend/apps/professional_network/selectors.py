from django.db.models import Q

from apps.demo_lab.selectors import is_demo_mode_enabled

from .models import ConnectionStatus, ProfessionalConnection, ProfessionalConversation


def connections_for_user(user):
    if not is_demo_mode_enabled():
        return ProfessionalConnection.objects.none()
    return ProfessionalConnection.objects.filter(
        Q(requester=user) | Q(recipient=user)
    ).select_related(
        "requester__identity_profile",
        "requester__professional_directory_profile",
        "recipient__identity_profile",
        "recipient__professional_directory_profile",
    )


def conversations_for_user(user):
    if not is_demo_mode_enabled():
        return ProfessionalConversation.objects.none()
    return ProfessionalConversation.objects.filter(
        Q(connection__requester=user) | Q(connection__recipient=user),
        connection__status=ConnectionStatus.ACCEPTED,
    ).select_related(
        "connection__requester__identity_profile",
        "connection__requester__professional_directory_profile",
        "connection__recipient__identity_profile",
        "connection__recipient__professional_directory_profile",
    )
