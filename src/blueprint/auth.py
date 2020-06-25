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
    """
    def post(self):
        """
        accepts user data and authorizes him
        :return: answer and status
        """
        request_json = request.json
        try:
            auth = scheme.auth.auth_schema.load(request_json)
        except ValidationError as ValEr:
            return jsonify(ValEr.messages), 400

        auth_service = AuthService(db.connection)
        try:
            auth_user = auth_service.authorization(auth)
        except UserNotFoundOrInfidelsData as user_er:
            return user_er.message, 404
        session['user_id'] = auth_user
        return {"answer": "Вы вошли в аккаунт"}, 200


class UserLogout(MethodView):
    """
    this class holds deauthorization user
    """
    def post(self):
        """
        deauthorization user
        :return: answer and status
        """
        session.pop('user_id', None)
        return {"answer": "Выход из аккаунта произведен"}, 200


bp.add_url_rule('/login', view_func=UserLogin.as_view('auth_login'))
bp.add_url_rule('/logout', view_func=UserLogout.as_view('auth_logout'))
