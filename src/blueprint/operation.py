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
from services.operation import InsertDataFaled, OperationOrCategoryNotFound
bp = Blueprint('operation', __name__)


class OperationView(MethodView):
    """
    class for add, delete, update, get operation
    :methods:
    post - add operation
    :param:
    user_id - id user in session

    patch - update operation
    :param:
    user_id - id user in session
    operation_id - id transfer operation

    delete - delete operation
    :param:
    user_id - id user in session
    operation_id - id transfer operation

    get - get operation
    :param:
    user_id - id user in session
    operation_id - id transfer operation
    """
    @auth_required
    def post(self, user_id):
        request_json = request.json
        try:
            operation = operation_schema.load(request_json)
        except ValidationError as ValEr:
            return jsonify(ValEr.messages), 400
        services = OperationServices(db.connection, user_id=user_id)
        try:
            operation_return = services.post_operation(operation)
        except InsertDataFaled:
            return {"answer": "Входные данные введены неверно"}, 400
        operation_return = get_operation_schema.dump(operation_return)
        return jsonify(operation_return), 200

    @auth_required
    def patch(self, operation_id, user_id):
        request_json = request.json
        try:
            operation = update_operation_schema.load(request_json)
        except ValidationError as ValEr:
            return jsonify(ValEr.messages), 400
        services = OperationServices(db.connection, operation_id=operation_id,
                                     user_id=user_id)
        try:
            operation_return = services.patch_operation(operation)
        except OperationOrCategoryNotFound:
            return {"answer": "Операции или категории не существует"}, 400
        operation_return = get_operation_schema.dump(operation_return)
        return jsonify(operation_return), 200

    @auth_required
    def delete(self, operation_id, user_id):
        services = OperationServices(db.connection, operation_id=operation_id,
                                     user_id=user_id)
        try:
            operation_return = services.del_operation()
        except OperationOrCategoryNotFound:
            return {"answer": "Операции не существует"}, 400
        return operation_return, 200

    @auth_required
    def get(self, operation_id, user_id):
        services = OperationServices(db.connection, operation_id=operation_id,
                                     user_id=user_id)
        try:
            operation_return = services.get_operation()
        except OperationOrCategoryNotFound:
            return {"answer": "Данной операции не существует"}, 400
        operation_return = get_operation_schema.dump(operation_return)
        return jsonify(operation_return), 200


bp.add_url_rule('', view_func=OperationView.as_view('operation'))
bp.add_url_rule('/<int:operation_id>', view_func=OperationView.
                as_view('change_operation'))

