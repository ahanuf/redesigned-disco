import json
import logging
from datetime import timedelta
import json
from datetime import timedelta

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ValidationError

from .models import Media, Message, Room
from .serializers import MessageSerializer

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope.get("user")

        # ---------------------------------------------------------
        # 1. Authentication
        # ---------------------------------------------------------

        if not user or user.is_anonymous:
            await self.close(code=4001)
            return

        # ---------------------------------------------------------
        # 2. Get room ID from URL
        # ---------------------------------------------------------

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]

        # ---------------------------------------------------------
        # 3. Verify room + membership
        # ---------------------------------------------------------

        room_exists = await self.user_is_room_member(
            self.room_id,
            user.pk,
        )

        if not room_exists:
            await self.close(code=4003)
            return

        # ---------------------------------------------------------
        # 4. Redis group
        # ---------------------------------------------------------

        self.room_group = f"chat_room_{self.room_id}"

        await self.channel_layer.group_add(
            self.room_group,
            self.channel_name,
        )

        await self.accept()

        # Tell the client the connection succeeded.
        await self.send(
            text_data=json.dumps(
                {
                    "type": "connection",
                    "status": "connected",
                    "room_id": self.room_id,
                }
            )
        )

    async def disconnect(self, close_code):
        if hasattr(self, "room_group"):
            await self.channel_layer.group_discard(
                self.room_group,
                self.channel_name,
            )

    # =============================================================
    # RECEIVE
    # =============================================================

    async def receive(self, text_data=None, bytes_data=None):

        if not text_data:
            return

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send_error("Invalid JSON.")
            return

        event_type = data.get("type")

        if event_type == "chat_message":
            await self.handle_new_message(data)

        elif event_type == "typing":
            await self.handle_typing(data)

        elif event_type == "status_update":
            await self.handle_status_update(data)

        elif event_type == "file":
            await self.handle_file_message(data)

        else:
            await self.send_error(
                "Unknown event type."
            )

    # =============================================================
    # CHAT MESSAGE
    # =============================================================

    async def handle_new_message(self, data):

        content = data.get("message", "")

        if not isinstance(content, str):
            await self.send_error(
                "Message must be text."
            )
            return

        content = content.strip()

        if not content:
            await self.send_error(
                "Message cannot be empty."
            )
            return

        # Prevent excessively large messages.
        if len(content) > 10000:
            await self.send_error(
                "Message is too long."
            )
            return

        # TTL validation.
        ttl = self.parse_ttl(data.get("ttl"))

        if data.get("ttl") is not None and ttl is None:
            await self.send_error(
                "Invalid TTL."
            )
            return

        message = await self.create_message(
            content=content,
            ttl=ttl,
        )

        serialized = await self.serialize_message(
            message
        )

        logger.warning(
            "BROADCASTING MESSAGE: room_group=%s message=%s",
            self.room_group,
            serialized,
        )

        await self.channel_layer.group_send(
            self.room_group,
            {
                "type": "chat.message",
                "message": serialized,
            },
        )

        logger.warning(
            "GROUP SEND COMPLETED: room_group=%s",
            self.room_group,
        )

        # Schedule ephemeral deletion.
        if ttl:

            from .tasks import delete_ephemeral

            delete_ephemeral.apply_async(
                args=[message.id],
                countdown=int(
                    ttl.total_seconds()
                ),
            )

    # =============================================================
    # TYPING
    # =============================================================

    async def handle_typing(self, data):

        status = data.get("status")

        if status not in ("started", "stopped"):
            await self.send_error(
                "Invalid typing status."
            )
            return

        await self.channel_layer.group_send(
            self.room_group,
            {
                "type": "chat.typing",
                "user_id": self.scope["user"].pk, # type: ignore
                "username": self.scope["user"].get_username(), # type: ignore
                "status": status,
            },
        )

    # =============================================================
    # MESSAGE STATUS
    # =============================================================

    async def handle_status_update(self, data):

        message_id = data.get("id")
        status = data.get("status")

        if not message_id:
            await self.send_error(
                "Message ID is required."
            )
            return

        if status not in ("delivered", "read"):
            await self.send_error(
                "Invalid message status."
            )
            return

        result = await self.update_message_status(
            message_id=message_id,
            status=status,
        )

        if not result:
            await self.send_error(
                "Message not found or access denied."
            )
            return

        await self.channel_layer.group_send(
            self.room_group,
            {
                "type": "chat.status",
                "id": message_id,
                "status": status,
                "user_id": self.scope["user"].pk, # type: ignore
                "username": self.scope["user"].get_username(), # type: ignore
            },
        )

    # =============================================================
    # FILE MESSAGE
    # =============================================================

    async def handle_file_message(self, data):

        media_id = data.get("media_id")

        if not media_id:
            await self.send_error(
                "media_id is required."
            )
            return

        message = await self.create_file_message(
            media_id=media_id,
        )

        if message is None:
            await self.send_error(
                "Invalid media or access denied."
            )
            return

        serialized = await self.serialize_message(
            message
        )

        await self.channel_layer.group_send(
            self.room_group,
            {
                "type": "chat.message",
                "message": serialized,
            },
        )

    # =============================================================
    # REDIS EVENT HANDLERS
    # =============================================================

    async def chat_message(self, event):

        logger.warning(
            "CHAT MESSAGE EVENT RECEIVED: channel=%s room=%s event=%s",
            self.channel_name,
            self.room_id,
            event,
        )

        await self.send(
            text_data=json.dumps(
                event["message"]
            )
        )

        logger.warning(
            "CHAT MESSAGE SENT TO CLIENT: channel=%s room=%s",
            self.channel_name,
            self.room_id,
        )

    async def chat_typing(self, event):

        await self.send(
            text_data=json.dumps(
                {
                    "type": "typing",
                    "user_id": event["user_id"],
                    "username": event["username"],
                    "status": event["status"],
                }
            )
        )

    async def chat_status(self, event):

        await self.send(
            text_data=json.dumps(
                {
                    "type": "status",
                    "id": event["id"],
                    "status": event["status"],
                    "user_id": event["user_id"],
                    "username": event["username"],
                }
            )
        )

    # =============================================================
    # DATABASE OPERATIONS
    # =============================================================

    @database_sync_to_async
    def user_is_room_member(
        self,
        room_id,
        user_id,
    ):

        return Room.objects.filter(
            pk=room_id,
            members__pk=user_id,
        ).exists()

    @database_sync_to_async
    def create_message(
        self,
        content,
        ttl,
    ):

        return Message.objects.create(
            room_id=self.room_id,
            user=self.scope["user"], # type: ignore
            content=content,
            ttl=ttl,
        )

    @database_sync_to_async
    def serialize_message(self, message):

        return MessageSerializer(
            message
        ).data

    @database_sync_to_async
    def update_message_status(
        self,
        message_id,
        status,
    ):
        message = (
            Message.objects
            .filter(
                pk=message_id,
                room_id=self.room_id,
            )
            .first()
        )

        if not message:
            return False

        # A user cannot mark their own message as delivered/read.
        if message.user_id == self.scope["user"].pk: # type: ignore
            return False

        if status == "delivered":
            if not message.delivered:
                message.delivered = True
                message.save(
                    update_fields=["delivered"]
                )

        elif status == "read":
            # Reading a message also means it was delivered.
            update_fields = []

            if not message.delivered:
                message.delivered = True
                update_fields.append("delivered")

            if not message.read:
                message.read = True
                update_fields.append("read")

            if update_fields:
                message.save(
                    update_fields=update_fields
                )

        return True

    @database_sync_to_async
    def create_file_message(
        self,
        media_id,
    ):

        media = (
            Media.objects
            .select_related("message")
            .filter(
                pk=media_id,
                uploaded_by=self.scope["user"],
            )
            .first()
        )

        if not media:
            return None

        # Prevent reusing media that has already been attached.
        if media.message_id is not None:
            return None

        message = Message.objects.create(
            room_id=self.room_id,
            user=self.scope["user"],
            content="",
        )

        media.message = message
        media.save(
            update_fields=["message"]
        )

        return message

    # =============================================================
    # VALIDATION
    # =============================================================

    @staticmethod
    def parse_ttl(raw_ttl):

        if raw_ttl is None:
            return None

        try:
            seconds = int(raw_ttl)
        except (TypeError, ValueError):
            return None

        # 0 is effectively not ephemeral.
        if seconds <= 0:
            return None

        # Maximum TTL: 30 days.
        max_seconds = 30 * 24 * 60 * 60

        if seconds > max_seconds:
            return None

        return timedelta(
            seconds=seconds
        )

    # =============================================================
    # ERROR RESPONSE
    # =============================================================

    async def send_error(self, message):

        await self.send(
            text_data=json.dumps(
                {
                    "type": "error",
                    "message": message,
                }
            )
        )