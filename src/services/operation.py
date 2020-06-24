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
from exceptions import ServiceError


class OperationDataError(ServiceError):
    """
    class exception with incorrect data
    """
    service = 'operation'


class EntityDoesNotExistError(OperationDataError):
    """
    class with the exception of a nonexistent entity
    """
    message = {"answer": "Cущности не существует"}, 404


class OperationServices:
    """
    сlass implements business logic various methods
    """
    def __init__(self, session, user_id=None, operation_id=None):
        """
        __init__ - class constructor
        :param session: connect to db
        :param user_id: user id in session
        :param operation_id: input operation id
        """
        self.session = session
        self.user_id = user_id
        self.operation_id = operation_id

    def create_operation(self, operation: Operation) -> GetOperation:
        """
        create_operation - adds operation to db
        :param operation: received data
        :return: dataclass with operation data
        """
        if operation.category_id is not None:
            category = (
                self.session.query(CategoryModel)
                    .filter(and_(
                            CategoryModel.id == operation.category_id,
                            CategoryModel.user_id == self.user_id))
                    .first())

            if category is None:
                raise EntityDoesNotExistError()

        new_operation = OperationModel(amount=(int(operation.amount * 100)),
                                       description=operation.description,
                                       datetime=operation.datetime,
                                       type_operation=operation.type_operation,
                                       user_id=self.user_id,
                                       category_id=operation.category_id)

        self.session.add(new_operation)
        self.session.commit()
        self.operation_id = new_operation.as_dict().get('id')
        return self.get_operation()

    def update_operation(self, operation: UpdateOperation) -> GetOperation:
        """
        update_operation - update record operation in db
        :param operation: received data
        :return: dataclass with operation data
        """
        category = True
        dict_operation = asdict(operation)
        dict_operation = {key: val for key, val in dict_operation.items()
                          if val is not None}

        operation = (
            self.session.query(OperationModel)
                .filter(and_(
                        OperationModel.id == self.operation_id,
                        OperationModel.user_id == self.user_id))
                .first())

        if dict_operation.get('category_id') is not None:
            category = (
                self.session.query(CategoryModel).filter
                (and_(CategoryModel.id == dict_operation.get('category_id'),
                      CategoryModel.user_id == self.user_id)).first()
            )

        if operation is None or category is None:
            raise EntityDoesNotExistError()

        if dict_operation.get('amount') is not None:
            amount = int(dict_operation.get('amount') * 100)
            del dict_operation['amount']
            dict_operation.update({'amount': amount})

        for key, value in dict_operation.items():
            setattr(operation, key, value)
        self.session.commit()
        return self.get_operation()

    def del_operation(self) -> dict:
        """
        del_operation - delete record operation in db
        :return: message dictionary
        """
        operation = (
            self.session.query(OperationModel)
                .filter(and_(
                        OperationModel.id == self.operation_id,
                        OperationModel.user_id == self.user_id))
                .delete())

        self.session.commit()
        if bool(operation) is False:
            raise EntityDoesNotExistError()

        return {"answer": "Операция удалена"}

    def get_operation(self) -> GetOperation:
        """
        get_operation - get record operation in db
        :return: dataclass with operation data
        """
        operation = (
            self.session.query(OperationModel)
                .filter(and_(
                        OperationModel.id == self.operation_id,
                        OperationModel.user_id == self.user_id))
                .first())

        if operation is None:
            raise EntityDoesNotExistError()

        dict_operation = operation.as_dict()
        dict_operation['amount'] = dict_operation.get('amount')/100

        return GetOperation(
            type_operation=dict_operation.get('type_operation'),
            amount=dict_operation.get('amount'),
            category_id=dict_operation.get('category_id'),
            datetime=dict_operation.get('datetime'),
            description=dict_operation.get('description'),
            id=dict_operation.get('id'),
            user_id=dict_operation.get('user_id')
            )
