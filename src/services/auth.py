"""
module with business logic for user authorization
:classes:
AuthService - this class allows produce authorization
"""
from models import AccountModel
from flask import session
from werkzeug.security import check_password_hash
from exceptions import SeviceError
from entities.auth import Auth


class AuthError(SeviceError):
    """
    class error auth for inherit
    """
    service = 'auth'


class UserNotFoundOrInfidelsData(AuthError):
    """
    class for exception, Invalid data or user does not exist
    """
    pass


class AuthService:
    """
    AuthService - this class allows produce authorization
    :methods:
    __init__ - class constructor
    post_auth - method accepts dateclass and authorize user
    """
    def __init__(self, session):
        self.session = session

    def post_auth(self, user: Auth) -> dict:
        user_data = self.session.query(AccountModel).filter\
            (AccountModel.email == user.email).first()

        if user_data is None or \
                not check_password_hash(user_data.password, user.password):
            raise UserNotFoundOrInfidelsData()

        user_data = user_data.as_dict()
        session['user_id'] = user_data.get('id')

        return {"answer": f"Вы вошли в аккаунт {user_data.get('email')}"}
