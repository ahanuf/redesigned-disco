from rest_framework import (
    parsers,
    permissions,
    status,
    viewsets,
)

from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Media,
    Message,
    Reaction,
    Room,
)

from .permissions import (
    IsMediaOwner,
    IsMessageOwner,
    IsReactionOwner,
    IsRoomCreator,
    IsRoomMember,
)

from .serializers import (
    MediaSerializer,
    MediaUploadSerializer,
    MessageSerializer,
    ReactionSerializer,
    RoomSerializer,
)


class RoomViewSet(viewsets.ModelViewSet):

    serializer_class = RoomSerializer

    def get_queryset(self):
        return (
            Room.objects
            .filter(
                members=self.request.user
            )
            .select_related("created_by")
            .prefetch_related("members")
        )

    def get_permissions(self):

        if self.action == "create":
            return [
                permissions.IsAuthenticated(),
            ]

        if self.action in [
            "update",
            "partial_update",
            "destroy",
            "add_member",
            "remove_member",
        ]:
            return [
                permissions.IsAuthenticated(),
                IsRoomCreator(),
            ]

        return [
            permissions.IsAuthenticated(),
            IsRoomMember(),
        ]

    def perform_create(self, serializer):

        room = serializer.save(
            created_by=self.request.user
        )

        room.members.add(
            self.request.user
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="add-member",
    )
    def add_member(self, request, pk=None):

        room = self.get_object()

        user_id = request.data.get("user_id")

        if not user_id:
            return Response(
                {
                    "detail": "user_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        from django.contrib.auth import get_user_model

        User = get_user_model()

        try:
            user = User.objects.get(
                pk=user_id
            )
        except User.DoesNotExist:
            return Response(
                {
                    "detail": "User not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if room.members.filter(
            pk=user.pk
        ).exists():

            return Response(
                {
                    "detail": "User is already a member."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        room.members.add(user)

        return Response(
            {
                "detail": "Member added.",
                "user_id": user.pk,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="remove-member",
    )
    def remove_member(self, request, pk=None):

        room = self.get_object()

        user_id = request.data.get("user_id")

        if not user_id:
            return Response(
                {
                    "detail": "user_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        from django.contrib.auth import get_user_model

        User = get_user_model()

        try:
            user = User.objects.get(
                pk=user_id
            )
        except User.DoesNotExist:
            return Response(
                {
                    "detail": "User not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.pk == room.created_by_id:

            return Response(
                {
                    "detail": "The room creator cannot be removed."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not room.members.filter(
            pk=user.pk
        ).exists():

            return Response(
                {
                    "detail": "User is not a member."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        room.members.remove(user)

        return Response(
            {
                "detail": "Member removed.",
                "user_id": user.pk,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="leave",
    )
    def leave(self, request, pk=None):

        room = self.get_object()

        if room.created_by_id == request.user.pk:

            return Response(
                {
                    "detail": (
                        "The room creator cannot leave "
                        "the room. Delete the room instead."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        room.members.remove(
            request.user
        )

        return Response(
            {
                "detail": "You left the room."
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["get"],
        url_path="members",
    )
    def members(self, request, pk=None):

        room = self.get_object()

        users = room.members.all()

        return Response(
            [
                {
                    "id": user.pk,
                    "username": user.get_username(),
                }
                for user in users
            ]
        )



class MessageViewSet(viewsets.ModelViewSet):

    serializer_class = MessageSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsRoomMember,
    ]

    def get_queryset(self):

        queryset = (
            Message.objects
            .filter(
                room__members=self.request.user
            )
            .select_related(
                "user",
                "room",
            )
            .prefetch_related(
                "media",
                "reactions",
            )
        )

        room_id = self.request.query_params.get("room")

        if room_id:
            queryset = queryset.filter(
                room_id=room_id
            )

        return queryset

    def perform_create(self, serializer):

        room = serializer.validated_data["room"]

        if not room.members.filter(
            pk=self.request.user.pk
        ).exists():
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "You are not a member of this room."
            )

        serializer.save(
            user=self.request.user
        )

    def get_permissions(self):

        if self.action in [
            "update",
            "partial_update",
            "destroy",
        ]:
            return [
                permissions.IsAuthenticated(),
                IsMessageOwner(),
            ]

        return super().get_permissions()


class MediaUploadView(viewsets.GenericViewSet):

    queryset = Media.objects.all()

    serializer_class = MediaSerializer

    parser_classes = [
        parsers.MultiPartParser,
    ]

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @action(
        detail=False,
        methods=["post"],
    )
    def upload(self, request):

        serializer = MediaUploadSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        media = serializer.save(
            uploaded_by=request.user
        )

        return Response(
            {
                "id": media.id,
                "url": media.file.url,
                "type": media.type,
            },
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self):

        return Media.objects.filter(
            uploaded_by=self.request.user
        )

    def get_permissions(self):

        if self.action in [
            "update",
            "partial_update",
            "destroy",
        ]:
            return [
                permissions.IsAuthenticated(),
                IsMediaOwner(),
            ]

        return super().get_permissions()


class ReactionViewSet(viewsets.ModelViewSet):

    serializer_class = ReactionSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsRoomMember,
    ]

    def get_queryset(self):

        return (
            Reaction.objects
            .filter(
                message__room__members=self.request.user
            )
            .select_related(
                "user",
                "message",
            )
        )

    def perform_create(self, serializer):

        message = serializer.validated_data["message"]

        if not message.room.members.filter(
            pk=self.request.user.pk
        ).exists():
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "You are not a member of this room."
            )

        serializer.save(
            user=self.request.user
        )

    def get_permissions(self):

        if self.action in [
            "update",
            "partial_update",
            "destroy",
        ]:
            return [
                permissions.IsAuthenticated(),
                IsReactionOwner(),
            ]

        return super().get_permissions()