"""
module with business logic for user registration and getting user
:classes:
UserService - class for registering and getting a user
"""
from models import AccountModel
from werkzeug.security import generate_password_hash
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
    message = {"answer": "Данный email уже используется"}


class UserService:
    """
    UserService - class for registering and getting a user
    """
    def __init__(self, session):
        """
        class constructor
        :param session: connect to db
        """
        self.session = session

    def create_user(self, user: UserCreate) -> User:
        """
        registering user
        :param user: dataclass with data for auth user
        :return: dataclass user
        """
        old_user = (self.session.query(AccountModel).filter
                    (AccountModel.email == user.email).first())

        if old_user is not None:
            raise ThisEmailAlreadyUse()

        password_hash = generate_password_hash(user.password)
        new_user = AccountModel(email=user.email, password=password_hash,
                                first_name=user.first_name,
                                last_name=user.last_name)
        self.session.add(new_user)
        self.session.commit()
        return self.get_user(new_user.as_dict().get('id'))

    def get_user(self, user_id: int) -> User:
        """
        getting user
        :param user_id: id user in session
        :return: dataclass user
        """
        data_user = (self.session.query(AccountModel).filter
                     (AccountModel.id == user_id).first())

        data_user = data_user.as_dict()
        return User(email=data_user.get('email'),
                    first_name=data_user.get('first_name'),
                    last_name=data_user.get('last_name'),
                    id=data_user.get('id')
                    )
