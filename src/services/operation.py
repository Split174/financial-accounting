"""
module with business logic for add/update/get/delete operation and
also contains exceptions
:clases:
OperationDateError - exception with incorrect data
InsertDataFaled - exception input data
OperationOrCategoryNotFound - exception when not found category or operation
OperationServices - сlass implements business logic various methods
"""
from models import OperationModel, CategoryModel
from entities.operation import GetOperation, UpdateOperation, Operation
from dataclasses import asdict
from sqlalchemy import and_
from datetime import datetime
from exceptions import SeviceError
import time


class OperationDataError(SeviceError):
    """
    class exception with incorrect data
    """
    service = 'operation'


class InsertDataFaled(OperationDataError):
    """
    class exception input data
    """
    pass


class OperationOrCategoryNotFound(OperationDataError):
    """
    class exception when not found category or operation
    """
    pass


class OperationServices:
    """
    сlass implements business logic various methods
    :methods:
    __init__ - class constructor
    :param:
    self.session - connect to db
    self.user_id - user id in session
    self.operation_id - input operation id

    post_operation - adds operation to db
    :param:
    operation - received data

    patch_operation - update record operation in db
    :param:
    operation - received data

    del_operation - delete record operation in db
    get_operation - get record operation in db
    """
    def __init__(self, session, user_id=None, operation_id=None):
        self.session = session
        self.user_id = user_id
        self.operation_id = operation_id

    def post_operation(self, operation: Operation) -> GetOperation:
        cur_time = int(time.mktime(
            time.strptime(str(operation.datetime), '%Y-%m-%d %H:%M:%S')))

        if operation.category_id is not None:
            category = self.session.query(CategoryModel).filter \
                (and_(CategoryModel.id == operation.category_id,
                      CategoryModel.user_id == self.user_id)).first()
            if category is None:
                raise InsertDataFaled()

        new_operation = OperationModel(amount=(operation.amount * 100),
                                       description=operation.description,
                                       datetime=cur_time,
                                       type_operation=operation.type_operation,
                                       user_id=self.user_id,
                                       category_id=operation.category_id)
        self.session.add(new_operation)
        self.session.commit()
        self.operation_id = new_operation.as_dict().get('id')
        return self.get_operation()

    def patch_operation(self, operation: UpdateOperation) -> GetOperation:
        category = True
        dict_operation = asdict(operation)
        dict_operation = {key: val for key, val in dict_operation.items()
                          if val is not None}

        operation = self.session.query(OperationModel).filter \
            (and_(OperationModel.id == self.operation_id,
                  OperationModel.user_id == self.user_id)).first()

        if dict_operation.get('category_id') is not None:
            category = self.session.query(CategoryModel).filter \
                (and_(CategoryModel.id == dict_operation.get('category_id'),
                      CategoryModel.user_id == self.user_id)).first()

        if operation is None or category is None:
            raise OperationOrCategoryNotFound()

        if dict_operation.get('amount') is not None:
            amount = dict_operation.get('amount') * 100
            del dict_operation['amount']
            dict_operation.update({'amount': amount})

        if dict_operation.get('datetime') is not None:
            cur_time = int(time.mktime(
                time.strptime(str(dict_operation.get('datetime')),
                              '%Y-%m-%d %H:%M:%S')))
            del dict_operation['datetime']
            dict_operation.update({'datetime': cur_time})

        for key, value in dict_operation.items():
            setattr(operation, key, value)
        self.session.commit()
        return self.get_operation()

    def del_operation(self) -> dict:
        operation = self.session.query(OperationModel).filter \
            (and_(OperationModel.id == self.operation_id,
                  OperationModel.user_id == self.user_id)).delete()
        self.session.commit()
        if bool(operation) is False:
            raise OperationOrCategoryNotFound()

        return {"answer": "Операция удалена"}

    def get_operation(self) -> GetOperation:
        print(self.operation_id)
        print(self.user_id)
        operation = self.session.query(OperationModel).filter \
            (and_(OperationModel.id == self.operation_id,
                  OperationModel.user_id == self.user_id)).first()
        if operation is None:
            raise OperationOrCategoryNotFound()
        str_time = time.strftime("%m-%d-%Y %H:%M:%S",
                                 time.localtime(operation.datetime))
        datetime_str = datetime.strptime(str_time, "%m-%d-%Y %H:%M:%S")
        dict_operation = operation.as_dict()
        dict_operation['amount'] = dict_operation.get('amount')/100
        del dict_operation['datetime']
        dict_operation.update({'datetime': str_time})

        return GetOperation(
            type_operation=dict_operation.get('type_operation'),
            amount=dict_operation.get('amount'),
            category_id=dict_operation.get('category_id'),
            datetime=datetime_str,
            description=dict_operation.get('description'),
            id=dict_operation.get('id'),
            user_id=dict_operation.get('user_id')
            )
