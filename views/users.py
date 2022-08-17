from flask import request
from flask_restx import Namespace, Resource

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')
user_schema = UserSchema()


@user_ns.route('/')
class UserView(Resource):

    def post(self):
        user_request = request.json
        new_user = user_service.create(**user_request)
        return user_schema.dump(new_user)
