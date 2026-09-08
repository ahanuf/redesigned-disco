from django.conf import settings
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_chat_rooms",
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="chat_rooms",
        blank=True,
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(
        Room,
        related_name="messages",
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_messages",
    )

    content = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

    delivered = models.BooleanField(default=False)

    read = models.BooleanField(default=False)

    ttl = models.DurationField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["timestamp"]

        indexes = [
            models.Index(fields=["room", "timestamp"]),
            models.Index(fields=["user", "timestamp"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.room} - {self.timestamp}"


class Media(models.Model):
    message = models.ForeignKey(
        Message,
        related_name="media",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_media",
    )

    file = models.FileField(
        upload_to="chat_media/",
    )

    type = models.CharField(
        max_length=10,
    )

    class Meta:
        indexes = [
            models.Index(fields=["uploaded_by"]),
        ]

    def __str__(self):
        return f"{self.type} - {self.file.name}"


class Reaction(models.Model):
    message = models.ForeignKey(
        Message,
        related_name="reactions",
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_reactions",
    )

    emoji = models.CharField(
        max_length=10,
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["message", "user", "emoji"],
                name="unique_message_user_emoji",
            ),
        ]

        indexes = [
            models.Index(fields=["message", "timestamp"]),
        ]

    def __str__(self):
        return f"{self.user} {self.emoji}"


class OfflineNotification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="offline_notifications",
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="offline_notifications",
    )

    title = models.CharField(
        max_length=255,
    )

    body = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    read = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ["-timestamp"]

        indexes = [
            models.Index(fields=["user", "read", "timestamp"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.title}"