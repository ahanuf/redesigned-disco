from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken


@database_sync_to_async
def get_user(validated_token):
    User = get_user_model()

    try:
        user_id = validated_token.get("user_id")

        if user_id is None:
            return AnonymousUser()

        return User.objects.get(pk=user_id)

    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"")
        query = parse_qs(query_string.decode())

        token = query.get("token", [None])[0]

        if token:
            try:
                validated_token = UntypedToken(token)
                scope["user"] = await get_user(validated_token)

            except Exception:
                scope["user"] = AnonymousUser()

        else:
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)


class JWTAuthMiddlewareInstance:

    def __init__(self, scope, inner):
        self.scope = dict(scope)
        self.inner = inner

    async def __call__(self, receive, send):

        query_string = self.scope.get("query_string", b"")
        query = parse_qs(query_string.decode())

        token = query.get("token", [None])[0]

        if token:
            try:
                validated_token = UntypedToken(token)

                self.scope["user"] = await get_user(
                    validated_token
                )

            except Exception:
                self.scope["user"] = AnonymousUser()

        else:
            self.scope["user"] = AnonymousUser()

        inner = self.inner(self.scope)

        return await inner(receive, send)