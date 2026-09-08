from rest_framework import permissions


class IsRoomMember(permissions.BasePermission):
    """
    Allow access only to authenticated users who are members
    of the relevant chat room.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        # Room object
        if hasattr(obj, "members"):
            return obj.members.filter(
                pk=user.pk
            ).exists()

        # Message / Reaction object
        if hasattr(obj, "room"):
            return obj.room.members.filter(
                pk=user.pk
            ).exists()

        # Media object
        if hasattr(obj, "message"):
            if obj.message is None:
                return obj.uploaded_by_id == user.pk

            return obj.message.room.members.filter(
                pk=user.pk
            ).exists()

        return False


class IsRoomCreator(permissions.BasePermission):
    """
    Only the room creator can modify or delete the room.
    """

    def has_object_permission(self, request, view, obj):

        if not request.user.is_authenticated:
            return False

        return obj.created_by_id == request.user.pk


class IsMessageOwner(permissions.BasePermission):
    """
    Only the message author can modify/delete a message.
    """

    def has_object_permission(self, request, view, obj):

        if not request.user.is_authenticated:
            return False

        return obj.user_id == request.user.pk


class IsReactionOwner(permissions.BasePermission):
    """
    Only the user who created a reaction can modify/delete it.
    """

    def has_object_permission(self, request, view, obj):

        if not request.user.is_authenticated:
            return False

        return obj.user_id == request.user.pk


class IsMediaOwner(permissions.BasePermission):
    """
    Only the uploader can modify/delete uploaded media.
    """

    def has_object_permission(self, request, view, obj):

        if not request.user.is_authenticated:
            return False

        return obj.uploaded_by_id == request.user.pk