"""
the module contains schemes for validation
:classes:
BaseSchema - class for inheritance
OperationSchema - class to validate added operation
UpdateOperationSchema - class to validate update operation
GetOperationSchema - class to validate getting operation
"""
from marshmallow import ValidationError, fields, validates
from entities.operation import Operation, GetOperation, UpdateOperation
from datetime import datetime, timezone
from scheme.base_scheme import BaseSchema


class OperationSchema(BaseSchema):
    """
    class to validate added operation
    :methods:
    validate_type_operation - validate add type operation
    """
    __entity_class__ = Operation
    type_operation = fields.String(required=True)
    amount = fields.Decimal(required=True)
    category_id = fields.Integer(missing=None)
    datetime = fields.DateTime(missing=lambda: datetime.now(tz=timezone.utc))
    description = fields.String(missing=None)

    @validates('type_operation')
    def validate_type_operation(self, data_type):
        if data_type != 'consumption' and data_type != 'income':
            raise ValidationError('Доступны операции consumption или income')

    @validates('amount')
    def validate_amount(self, amount):
        if amount < 0:
            raise ValidationError('Ввод отрицательного числа запрещен')


class UpdateOperationSchema(BaseSchema):
    """
    class to validate update operation
    """
    __entity_class__ = UpdateOperation
    type_operation = fields.String(missing=None)
    amount = fields.Decimal(missing=None)
    category_id = fields.Integer(missing=None)
    datetime = fields.DateTime(missing=None)
    description = fields.String(missing=None)


class GetOperationSchema(BaseSchema):
    """
    class to validate get operation
    """
    __entity_class__ = GetOperation
    id = fields.Integer(required=True)
    type_operation = fields.String(required=True)
    amount = fields.Decimal(required=True, as_string=True)
    user_id = fields.Integer(required=True)
    category_id = fields.Integer()
    datetime = fields.DateTime()
    description = fields.String()


get_operation_schema = GetOperationSchema()
operation_schema = OperationSchema()
update_operation_schema = UpdateOperationSchema()
