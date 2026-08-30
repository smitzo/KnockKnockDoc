from django.urls import path

from .views import (
    ConnectionListCreateView,
    ConnectionTransitionView,
    ConversationListView,
    ConversationMessageView,
    ProfessionalDirectoryListView,
)

urlpatterns = [
    path("doctors/", ProfessionalDirectoryListView.as_view(), name="network-doctors"),
    path("connections/", ConnectionListCreateView.as_view(), name="network-connections"),
    path(
        "connections/<uuid:connection_id>/<str:action>/",
        ConnectionTransitionView.as_view(),
        name="network-connection-transition",
    ),
    path("conversations/", ConversationListView.as_view(), name="network-conversations"),
    path(
        "conversations/<uuid:conversation_id>/messages/",
        ConversationMessageView.as_view(),
        name="network-conversation-messages",
    ),
]
