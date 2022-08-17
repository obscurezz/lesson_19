import base64
import hashlib

from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def _generate_password_digest(self, password: str) -> bytes:
        return hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode("utf-8"),
            salt=PWD_HASH_SALT,
            iterations=PWD_HASH_ITERATIONS,
        )

    def generate_password_hash(self, password: str) -> str:
        return base64.b64encode(self._generate_password_digest(password)).decode('utf-8')

    def get_all_users(self):
        return self.dao.get_all()

    def get_one_by_arguments(self, username: str, password: str):
        hashed_password = self.generate_password_hash(password)
        return self.dao.get_one_by_arguments(username, hashed_password)

    def get_one_user(self, user_id: int):
        return self.dao.get_one(user_id)

    def create(self, **kwargs):
        hash_pass = self.generate_password_hash(kwargs['password'])
        kwargs['password'] = hash_pass

        return self.dao.create(**kwargs)

    def update(self, **kwargs):
        if 'password' in kwargs.keys():
            hash_pass = self.generate_password_hash(kwargs['password'])
            kwargs['password'] = hash_pass

        self.dao.update(**kwargs)
        return self.dao

    def delete(self, user_id):
        self.dao.delete(user_id)

