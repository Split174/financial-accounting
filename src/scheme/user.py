"""
module for validating authorization data
:classes:
BaseSchema - parent class to inherit
UserAuthSchema - class for validating registration data
GetUserAuthSchema - the class validates and passes data
"""
from marshmallow import Schema, fields, validate, post_load
from entities.user import UserCreate, User


class BaseSchema(Schema):
    """
    BaseSchema - class for validating authorization data
    :methods:
    make_object - transfers data to convert to dataclass
    """
    __entity_class__ = None

    @post_load
    def make_object(self, data, **kwargs):
        return self.__entity_class__(**data)


class UserAuthSchema(BaseSchema):
    """
    AuthSchema - class for validating registration data
    """
    __entity_class__ = UserCreate
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)


class GetUserAuthSchema(BaseSchema):
    """
    AuthSchema - class for validating getting user data
    """
    __entity_class__ = User
    id = fields.Integer(required=True)
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)


get_user_schema = GetUserAuthSchema()
user_schema = UserAuthSchema()
