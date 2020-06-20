"""
module for validating authorization data
:classes:
AuthSchema - class for validating authorization data
"""
from marshmallow import Schema, fields, validate, post_load
from entities.auth import Auth


class AuthSchema(Schema):
    """
    AuthSchema - class for validating authorization data
    :methods:
    make_object - transfers data to convert to dataclass
    """
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))

    @post_load
    def make_object(self, data, **kwargs):
        return Auth(**data)


auth_schema = AuthSchema()
