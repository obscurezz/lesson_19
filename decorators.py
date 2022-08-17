from typing import Callable

import jwt
from flask import request, abort
from constants import SECRET


def auth_required(func: Callable):
    def decorator(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        auth_data = request.headers['Authorization']
        token = auth_data.split('Bearer ')[-1]

        try:
            jwt.decode(token, SECRET, algorithms=['HS256'])
        except jwt.exceptions.DecodeError as e:
            abort(401)
            return {'Exception': e}

        return func(*args, **kwargs)

    return decorator


def admin_required(func: Callable):
    def decorator(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        auth_data = request.headers['Authorization']
        token = auth_data.split('Bearer ')[-1]

        try:
            user = jwt.decode(token, SECRET, algorithms=['HS256'])
            user_role = user.get('role', 'user')
        except jwt.exceptions.DecodeError as e:
            abort(401)
            return {'Exception': e}

        if user_role != 'admin':
            abort(403)

        return func(*args, **kwargs)

    return decorator
