"""
module with business logic for user registration and getting user
:classes:
UserService - class for registering and getting a user
"""
from models import AccountModel
from werkzeug.security import generate_password_hash
from flask import session
from exceptions import ServiceError
from entities.user import UserCreate, User


class UserError(ServiceError):
    """
    class for inherit exception
    """
    service = 'user'


class ThisEmailAlreadyUse(UserError):
    """
    class with conflict error email
    """
    pass


class UserService:
    """
    UserService - class for registering and getting a user
    :methods:
    __init__ - class constructor
    post_user - registering user
    :param:
    user - dataclass with data for auth user
    get_user - getting user
    """
    def __init__(self, session):
        self.session = session

    def post_user(self, user: UserCreate) -> dict:
        old_user = self.session.query(AccountModel).filter\
            (AccountModel.email == user.email).first()

        if old_user is not None:
            raise ThisEmailAlreadyUse()

        password_hash = generate_password_hash(user.password)
        new_user = AccountModel(email=user.email, password=password_hash,
                                first_name=user.first_name,
                                last_name=user.last_name)
        self.session.add(new_user)
        self.session.commit()
        return {"answer": "аккаунт создан"}

    def get_user(self) -> User:
        data_user = self.session.query(AccountModel).filter\
            (AccountModel.id == dict(session).get('user_id')).first()
        data_user = data_user.as_dict()
        return User(email=data_user.get('email'),
                    first_name=data_user.get('first_name'),
                    last_name=data_user.get('last_name'),
                    id=data_user.get('id')
                    )
