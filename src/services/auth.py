"""
module with business logic for user authorization
:classes:
AuthService - this class allows produce authorization
"""
from models import AccountModel
from werkzeug.security import check_password_hash
from exceptions import ServiceError
from entities.auth import Auth


class AuthError(ServiceError):
    """
    class error auth for inherit
    """
    service = 'auth'


class UserNotFoundOrInfidelsData(AuthError):
    """
    class for exception, Invalid data or user does not exist
    """
    message = {"answer": "Данного пользователя не существует "
                         "или введены неверные данные"}


class AuthService:
    """
    AuthService - this class allows produce authorization
    """
    def __init__(self, session):
        """
        class constructor
        :param session: connect to db
        """
        self.session = session

    def authorization(self, user: Auth) -> int:
        """
        method accepts dateclass and authorize user
        :param user: authorization data
        :return: user id
        """
        user_data = (self.session.query(AccountModel).filter
                     (AccountModel.email == user.email).first())

        if (user_data is None or
                not check_password_hash(user_data.password, user.password)):
            raise UserNotFoundOrInfidelsData()

        user_id = user_data.as_dict().get('id')
        return user_id
