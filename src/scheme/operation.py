"""
the module contains schemes for validation
:classes:
BaseSchema - class for inheritance
OperationSchema - class to validate added operation
UpdateOperationSchema - class to validate update operation
GetOperationSchema - class to validate getting operation
"""
from marshmallow import Schema, ValidationError, fields, post_load, validates
from entities.operation import Operation, GetOperation, UpdateOperation
from datetime import datetime


class BaseSchema(Schema):
    """
    class for inheritance and and transfers to dataclass
    :methods:
    make_object - convert to dataclass
    """
    __entity_class__ = None

    @post_load
    def make_object(self, data, **kwargs):
        return self.__entity_class__(**data)


class OperationSchema(BaseSchema):
    """
    class to validate added operation
    :methods:
    validate_type_operation - validate add type operation
    """
    __entity_class__ = Operation
    type_operation = fields.String(required=True)
    amount = fields.Integer(required=True)
    category_id = fields.Integer(missing=None)
    datetime = fields.DateTime(format="%m-%d-%Y %H:%M:%S",
                               missing=int(datetime.now().timestamp()))
    description = fields.String(missing=None)

    @validates('type_operation')
    def validate_type_operation(self, data_type):
        if data_type != 'расход' and data_type != 'доход':
            raise ValidationError('Доступны операции расход или доход')


class UpdateOperationSchema(BaseSchema):
    """
    class to validate update operation
    """
    __entity_class__ = UpdateOperation
    type_operation = fields.String(missing=None)
    amount = fields.Integer(missing=None)
    category_id = fields.Integer(missing=None)
    datetime = fields.DateTime(format="%m-%d-%Y %H:%M:%S", missing=None)
    description = fields.String(missing=None)


class GetOperationSchema(BaseSchema):
    """
    class to validate get operation
    """
    __entity_class__ = GetOperation
    id = fields.Integer(required=True)
    type_operation = fields.String(required=True)
    amount = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    category_id = fields.Integer()
    datetime = fields.DateTime(format="%m-%d-%Y %H:%M:%S")
    description = fields.String()


get_operation_schema = GetOperationSchema()
operation_schema = OperationSchema()
update_operation_schema = UpdateOperationSchema()
