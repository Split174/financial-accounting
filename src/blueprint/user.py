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
from services.user import UserService as UserService
from auth_required import auth_required

bp = Blueprint('user', __name__)


class UserView(MethodView):
    """
    class for registering and gets a user
    :methods:
    post - receives user data and registers him
    get - returns user data
    """
    def post(self):
        request_json = request.json
        try:
            user = scheme.user.user_schema.load(request_json)
        except ValidationError as ValidEr:
            return jsonify(ValidEr.messages), 400
        service = UserService(db.connection)
        user = service.post_user(user=user)
        return user

    @auth_required
    def get(self):
        service = UserService(db.connection)
        user = service.get_user()
        user_return = scheme.user.get_user_schema.dump(user)
        return user_return, 200


bp.add_url_rule('', view_func=UserView.as_view('user'))