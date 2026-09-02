from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.identity.permissions import HasActiveIdentity

from ..models import ProfessionalDirectoryProfile
from ..permissions import IsVerifiedProfessional
from ..selectors import connections_for_user, conversations_for_user
from ..services import (
    ConnectionRequestCommand,
    append_message,
    request_connection,
    transition_connection,
)
from .serializers import (
    ConnectionCreateSerializer,
    ConnectionSerializer,
    ConversationSerializer,
    MessageCreateSerializer,
    MessageSerializer,
    ProfessionalCardSerializer,
)


class NetworkPagination(PageNumberPagination):
    page_size = 24
    page_size_query_param = "page_size"
    max_page_size = 50


class NetworkPermissionMixin:
    permission_classes = [HasActiveIdentity, IsVerifiedProfessional]
    throttle_classes = [ScopedRateThrottle]


class ProfessionalDirectoryListView(NetworkPermissionMixin, ListAPIView):
    serializer_class = ProfessionalCardSerializer
    pagination_class = NetworkPagination
    throttle_scope = "network_directory"

    def get_queryset(self):
        queryset = ProfessionalDirectoryProfile.objects.select_related(
            "user__identity_profile"
        ).annotate(
            rating_count_value=Count("ratings", distinct=True),
            communication_rating=Avg("ratings__communication_score"),
            collaboration_rating=Avg("ratings__collaboration_score"),
            handback_rating=Avg("ratings__handback_score"),
        ).filter(
            is_discoverable=True,
            is_synthetic=True,
        ).exclude(user=self.request.user)
        query = self.request.query_params.get("q", "").strip()[:80]
        specialty = self.request.query_params.get("specialty", "").strip()[:80]
        country = self.request.query_params.get("country", "").strip()[:80]
        if query:
            queryset = queryset.filter(
                Q(user__identity_profile__display_name__icontains=query)
                | Q(specialty__icontains=query)
                | Q(country__icontains=query)
                | Q(city__icontains=query)
                | Q(organization_name__icontains=query)
            )
        if specialty:
            queryset = queryset.filter(specialty=specialty)
        if country:
            queryset = queryset.filter(country=country)
        return queryset.order_by("user__identity_profile__display_name", "id")


class ConnectionListCreateView(NetworkPermissionMixin, APIView):
    throttle_scope = "network_connection"

    def get(self, request):
        connections = connections_for_user(request.user)
        return Response(
            ConnectionSerializer(connections, many=True, context={"request": request}).data
        )

    def post(self, request):
        serializer = ConnectionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        connection = request_connection(
            actor=request.user,
            command=ConnectionRequestCommand(
                recipient_profile_id=str(serializer.validated_data["recipient_profile_id"]),
                purpose=serializer.validated_data["purpose"],
                note=serializer.validated_data.get("note", ""),
            ),
        )
        connection = connections_for_user(request.user).get(id=connection.id)
        return Response(
            ConnectionSerializer(connection, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class ConnectionTransitionView(NetworkPermissionMixin, APIView):
    throttle_scope = "network_connection"

    def post(self, request, connection_id, action):
        connection = transition_connection(
            actor=request.user,
            connection_id=connection_id,
            action=action,
        )
        connection = connections_for_user(request.user).get(id=connection.id)
        return Response(ConnectionSerializer(connection, context={"request": request}).data)


class ConversationListView(NetworkPermissionMixin, APIView):
    throttle_scope = "network_message"

    def get(self, request):
        conversations = conversations_for_user(request.user)
        return Response(
            ConversationSerializer(
                conversations,
                many=True,
                context={"request": request},
            ).data
        )


class ConversationMessageView(NetworkPermissionMixin, APIView):
    throttle_scope = "network_message"

    def get_conversation(self, request, conversation_id):
        return get_object_or_404(conversations_for_user(request.user), id=conversation_id)

    def get(self, request, conversation_id):
        conversation = self.get_conversation(request, conversation_id)
        messages = conversation.messages.select_related("sender__identity_profile")[:200]
        return Response(MessageSerializer(messages, many=True, context={"request": request}).data)

    def post(self, request, conversation_id):
        conversation = self.get_conversation(request, conversation_id)
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = append_message(
            actor=request.user,
            conversation=conversation,
            body=serializer.validated_data["body"],
        )
        return Response(
            MessageSerializer(message, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )
