import base64
import calendar
import datetime
import hmac
from typing import Union

import jwt

from service.user import UserService
from constants import SECRET
from flask import abort


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def compose_passwords(self, password_hash: Union[str, bytes], password: str) -> bool:
        decoded_digest: bytes = base64.b64decode(password_hash)

        hash_digest: bytes = self.user_service._generate_password_digest(password)

        return hmac.compare_digest(decoded_digest, hash_digest)

    def _generate_tokens(self, username: str, password: str | None, is_refresh: bool = False) -> dict:
        user = self.user_service.get_all_users(username=username)
        if not user:
            abort(404)

        if not is_refresh:
            if not self.compose_passwords(user.password, password):
                abort(400)

        data = {
            'username': user.username,
            'role': user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET, algorithm='HS256')

        days30 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        data['exp'] = calendar.timegm(days30.timetuple())
        refresh_token = jwt.encode(data, SECRET, algorithm='HS256')

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def _approve_refresh_token(self, refresh_token: str) -> dict:
        data = jwt.decode(refresh_token, SECRET, algorithms=['HS256'])
        username = data.get('username')

        return self._generate_tokens(username, None, is_refresh=True)
