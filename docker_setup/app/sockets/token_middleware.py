from urllib import parse
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.auth import AuthMiddlewareStack
from .models import ChatRoom


@database_sync_to_async
def get_user_from_headers_or_queries(scope):
    print("=============hhh")
    try:
        path_value = scope.get('path', '')
        number = path_value.split('/')[-2]
        room_id = int(number)
        room=ChatRoom.objects.get(id=room_id)
    except:
        #pass
        return None

    try:
        headers = dict(scope["headers"])
    except KeyError as error:
        headers = {}

    try:
        params = dict(parse.parse_qsl(scope["query_string"].decode("utf8")))
    except KeyError as error:
        params = {}

    token_key = None
    token_is_found = False

    if b"authorization" in headers:
        token_name, token_key = headers[b"authorization"].decode().split()
        if token_name == "Token":
            token_is_found = True
    else:
        token_key = params.get("token")
        token_is_found = True if token_key else False

    if token_is_found:
        from rest_framework_simplejwt.authentication import JWTAuthentication
        from rest_framework_simplejwt.tokens import AccessToken
        from rest_framework.exceptions import AuthenticationFailed

        try:
            validated_token = AccessToken(token_key)
            user = JWTAuthentication().get_user(validated_token)
            if user == room.participant1 or user == room.participant2 :
                return user
            else:
                pass
        except Exception as e:
            print(e)
    return None


class TokenAuthMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        user = await get_user_from_headers_or_queries(scope)
        if user is not None:
            scope["user"] = user
        return await self.app(scope, receive, send)



def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))


