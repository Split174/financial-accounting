"""
this module allows you to create and receive a user
:classes:
UserView - class for registering and gets a user
"""
from marshmallow import ValidationError
import scheme.user
from flask import (
    Blueprint,
    request,
    jsonify
)
from flask.views import MethodView
from database import db
from services.user import UserService
from auth_required import auth_required
from services.user import ThisEmailAlreadyUse
bp = Blueprint('user', __name__)


class UserView(MethodView):
    """
    class for registering and gets a user
    """
    def post(self):
        """
        receives user data and registers him
        :return: data user in josn format
        """
        request_json = request.json
        try:
            user = scheme.user.user_schema.load(request_json)
        except ValidationError as ValidEr:
            return jsonify(ValidEr.messages), 400
        service = UserService(db.connection)
        try:
            user = service.create_user(user=user)
        except ThisEmailAlreadyUse as email_er:
            return email_er.message, 400
        return jsonify(scheme.user.get_user_schema.dump(user)), 201

    @auth_required
    def get(self, user_id):
        """
        returns user data
        :param user_id: id user in session
        :return: data user in josn format
        """
        service = UserService(db.connection)
        user = service.get_user(user_id=user_id)
        return jsonify(scheme.user.get_user_schema.dump(user)), 200


bp.add_url_rule('', view_func=UserView.as_view('user'))
