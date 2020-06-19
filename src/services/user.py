"""
module with business logic for user registration and getting user
:classes:
UserService - class for registering and getting a user
"""
from models import AccountModel
from werkzeug.security import generate_password_hash
from flask import session
import scheme.user


class UserService:
    """
    UserService - class for registering and getting a user
    :methods:
    __init__ - class constructor
    post_user - registering user
    get_user - getting user
    """
    def __init__(self, session):
        self.session = session

    def post_user(self, user):
        old_user = self.session.query(AccountModel).filter\
            (AccountModel.email == user.email).first()

        if old_user is not None:
            return {"answer": "Данный email уже используется"}, 400

        password_hash = generate_password_hash(user.password)
        new_user = AccountModel(email=user.email, password=password_hash,
                                first_name=user.first_name,
                                last_name=user.last_name)
        self.session.add(new_user)
        self.session.commit()
        return {"answer": "аккаунт создан"}, 201

    def get_user(self):
        data_user = self.session.query(AccountModel).filter\
            (AccountModel.id == dict(session).get('user_id')).first()
        data_user = data_user.as_dict()
        user_schema = scheme.user.get_user_schema.load(data_user)
        return user_schema
