"""
This module makes it possible to authorize and deauthorization a user
:classes:
UserLogin - user authorization
UserLogout - user deauthorization
"""
import scheme.auth
from flask import (
    Blueprint,
    request,
    session,
    jsonify
)
from marshmallow import ValidationError
from database import db
from services.auth import AuthService
from flask.views import MethodView
from services.auth import UserNotFoundOrInfidelsData

bp = Blueprint('auth', __name__)


class UserLogin(MethodView):
    """
    this class holds authorization user
    :methods:
    post - accepts user data and authorizes him
    """
    def post(self):
        request_json = request.json
        try:
            auth = scheme.auth.auth_schema.load(request_json)
        except ValidationError as ValEr:
            return jsonify(ValEr.messages), 400

        auth_service = AuthService(db.connection)
        try:
            auth_user = auth_service.post_auth(auth)
        except UserNotFoundOrInfidelsData:
            return {"answer": "Данного пользователя не существует"
                              " или введены неверные данные"}, 400
        return auth_user, 200


class UserLogout(MethodView):
    """
    this class holds deauthorization user
    :methods:
    post - deauthorization user
    """
    def post(self):
        session.pop('user_id', None)
        return {"answer": "Выход из аккаунта произведен"}, 200


bp.add_url_rule('/login', view_func=UserLogin.as_view('auth_login'))
bp.add_url_rule('/logout', view_func=UserLogout.as_view('auth_logout'))
