"""
module for validating authorization data
:classes:
BaseSchema - parent class to inherit
UserAuthSchema - class for validating registration data
GetUserAuthSchema - the class validates and passes data
"""
from marshmallow import fields, validate
from entities.user import UserCreate, User
from scheme.base_scheme import BaseSchema


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
    id = fields.Integer()
    email = fields.Email()
    first_name = fields.String()
    last_name = fields.String()


get_user_schema = GetUserAuthSchema()
user_schema = UserAuthSchema()
