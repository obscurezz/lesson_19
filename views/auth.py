from flask import request
from flask_restx import Resource, Namespace

from implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    @staticmethod
    def post():
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if None in (username, password):
            return '', 400

        tokens = auth_service._generate_tokens(username, password)
        return tokens, 201

    @staticmethod
    def put():
        refresh_token = request.json.get('refresh_token')
        tokens = auth_service._approve_refresh_token(refresh_token)
        return tokens, 201
