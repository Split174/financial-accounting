"""
module for validating authorization data
:classes:
AuthSchema - class for validating authorization data
"""
from marshmallow import fields, validate
from scheme.base_scheme import BaseSchema
from entities.auth import Auth


class AuthSchema(BaseSchema):
    """
    class for validating authorization data
    """
    __entity_class__ = Auth
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))


auth_schema = AuthSchema()
