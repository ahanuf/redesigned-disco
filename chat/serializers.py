from rest_framework import serializers

from .models import (
    Media,
    Message,
    Reaction,
    Room,
)


class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media

        fields = [
            "id",
            "message",
            "file",
            "type",
            "uploaded_by",
        ]

        read_only_fields = [
            "id",
            "message",
            "uploaded_by",
        ]


class MediaUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media

        fields = [
            "id",
            "file",
            "type",
            "uploaded_by",
        ]

        read_only_fields = [
            "id",
            "uploaded_by",
        ]


class ReactionSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Reaction

        fields = [
            "id",
            "message",
            "user",
            "emoji",
            "timestamp",
        ]

        read_only_fields = [
            "id",
            "user",
            "timestamp",
        ]


class MessageSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(
        read_only=True
    )

    media = MediaSerializer(
        many=True,
        read_only=True,
    )

    reactions = ReactionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Message

        fields = [
            "id",
            "room",
            "user",
            "content",
            "timestamp",
            "delivered",
            "read",
            "ttl",
            "media",
            "reactions",
        ]

        read_only_fields = [
            "id",
            "user",
            "timestamp",
            "delivered",
            "read",
            "media",
            "reactions",
        ]


class RoomSerializer(serializers.ModelSerializer):

    members = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    created_by = serializers.StringRelatedField(
        read_only=True
    )

    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Room

        fields = [
            "id",
            "name",
            "created_by",
            "members",
            "member_count",
            "created",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "members",
            "member_count",
            "created",
        ]

    def get_member_count(self, obj):
        return obj.members.count()