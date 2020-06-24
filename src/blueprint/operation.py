"""
this module allows you to create, update, delete and receive an operation
:classes:
OperationView - this class allows you to create, update,
delete and receive an operation
"""
from flask.views import MethodView
from flask import jsonify, request, Blueprint
from marshmallow import ValidationError
from scheme.operation import (operation_schema,
                              update_operation_schema,
                              get_operation_schema)
from auth_required import auth_required
from services.operation import OperationServices
from database import db
from services.operation import EntityDoesNotExistError
bp = Blueprint('operation', __name__)


class OperationView(MethodView):
    """
    class for add, delete, update, get operation
    """
    @auth_required
    def post(self, user_id):
        """
        add operation
        :param user_id: id user in session
        :return: transaction data in the format json
        """
        request_json = request.json
        try:
            operation = operation_schema.load(request_json)
        except ValidationError as val_er:
            return jsonify(val_er.messages), 400
        services = OperationServices(db.connection, user_id=user_id)
        try:
            operation_return = services.create_operation(operation)
        except EntityDoesNotExistError as entity_er:
            return entity_er.message
        operation_return = get_operation_schema.dump(operation_return)
        return jsonify(operation_return), 200

    @auth_required
    def patch(self, operation_id, user_id):
        """
        update operation
        :param operation_id: id transfer operation
        :param user_id: id user in session
        :return: transaction data in the format json
        """
        request_json = request.json
        try:
            operation = update_operation_schema.load(request_json)
        except ValidationError as val_er:
            return jsonify(val_er.messages), 400
        services = OperationServices(db.connection, operation_id=operation_id,
                                     user_id=user_id)
        try:
            operation_return = services.update_operation(operation)
        except EntityDoesNotExistError as entity_er:
            return entity_er.message
        operation_return = get_operation_schema.dump(operation_return)
        return jsonify(operation_return), 200

    @auth_required
    def delete(self, operation_id, user_id):
        """
        delete operation
        :param operation_id: id transfer operation
        :param user_id: id user in session
        :return: message in format dict
        """
        services = OperationServices(db.connection, operation_id=operation_id,
                                     user_id=user_id)
        try:
            operation_return = services.del_operation()
        except EntityDoesNotExistError as entity_er:
            return entity_er.message
        return operation_return, 200

    @auth_required
    def get(self, operation_id, user_id):
        """
        get operation
        :param operation_id: id transfer operation
        :param user_id: id user in session
        :return: transaction data in the format json
        """
        services = OperationServices(db.connection, operation_id=operation_id,
                                     user_id=user_id)
        try:
            operation_return = services.get_operation()
        except EntityDoesNotExistError as entity_er:
            return entity_er.message
        operation_return = get_operation_schema.dump(operation_return)
        return jsonify(operation_return), 200


bp.add_url_rule('', view_func=OperationView.as_view('operation'))
bp.add_url_rule('/<int:operation_id>', view_func=OperationView.
                as_view('change_operation'))

