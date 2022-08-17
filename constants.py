import secrets
import os

PWD_HASH_SALT = secrets.token_hex(8).encode('utf-8')
PWD_HASH_ITERATIONS = 100_000
SECRET = os.urandom(12)
