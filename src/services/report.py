"""
module contains business logic for get report
:classes:
ReportService - сlass implements business logic get methods
ReportDataError - class exception with incorrect data
ReportCategoryError - class with the exception of a nonexistent entity
"""
from models import OperationModel, CategoryModel, LevelCategoryModel
from sqlalchemy import func, and_, between
from datetime import datetime
from ready_date import get_date
from entities.report import ReportOperation, CategoryOperation, ReportGet, Report
from exceptions import ServiceError
from typing import List


class ReportDataError(ServiceError):
    """
    class exception with incorrect data
    """
    service = 'report'


class ReportCategoryError(ReportDataError):
    """
    class with the exception of a nonexistent entity
    """
    message = {"answer": "Cущности не существует"}


class ReportService:
    """
    сlass implements business logic get methods
    """
    def __init__(self, session, user_id):
        """
        class constructor
        :param session: connect to db
        :param user_id: user id in session
        """
        self.session = session
        self.user_id = user_id

    def get_report(self, report: Report) -> ReportGet:
        """
        generates a report on the specified parameters
        :param report: data for search
        :return: dataclass report
        """
        report.page = ((report.page - 1) * report.page_size)
        if report.category_name is not None:
            report.category_name = report.category_name.lower()

        query = (
            self.session.query(OperationModel)
                .filter(OperationModel.user_id == self.user_id)
                .order_by(OperationModel.datetime.desc())
           )

        if report.category_name is None:
            query = query.outerjoin(CategoryModel,
                                    OperationModel.category_id ==
                                    CategoryModel.id)
        else:

            query_category_id = (
                self.session.query(CategoryModel.id)
                .filter(and_(CategoryModel.name == report.category_name,
                             CategoryModel.user_id == self.user_id)).scalar()
            )

            if query_category_id is None:
                raise ReportCategoryError

            tree = self.__get_category_by_id(query_category_id)
            query = (
                query.join(CategoryModel,
                           OperationModel.category_id ==
                           CategoryModel.id)
                     .filter(CategoryModel.id.in_(tree))
            )

        if report.ready_date is not None:
            if report.ready_date == 'all_time':
                pass
            else:
                date_today = datetime.now()
                start_date, finish_date = get_date(date_today, report.ready_date)

                query = query.filter(between(OperationModel.datetime,
                                             start_date, finish_date))

        elif report.start_date is not None and report.finish_date is not None:
            query = query.filter(between(OperationModel.datetime,
                                         report.start_date,
                                         report.finish_date))

        query = query.limit(report.page_size).offset(report.page).all()

        operations = []
        id_sum_list = []
        for record in query:
            categories = None
            if record.category_id is not None:
                categories = self.__get_up_category_tree(record.category_id)
            amount = record.amount
            if amount is not None:
                amount = amount / 100
            operations.append(ReportOperation(amount=amount,
                                              description=record.description,
                                              datetime=record.datetime,
                                              category=categories))
            id_sum_list.append(record.id)
        result_sum = ((
                        self.session.query(func.sum(OperationModel.amount))
                            .filter(and_(OperationModel.id.in_(id_sum_list),
                                         OperationModel.type_operation ==
                                         'consumption'))).scalar())
        if result_sum is not None:
            result_sum = result_sum / 100

        return ReportGet(operation=operations, result_sum=result_sum)

    def __get_category_by_id(self, category_id: int) -> list:
        """
        builds a category tree
        :param category_id: id parent category
        :return: list category tree
        """
        tree = []
        children = (
            self.session.query(LevelCategoryModel)
                .filter(LevelCategoryModel.parent_id == category_id).all())
        tree.append(category_id)
        for child in children:
            a = self.__get_category_by_id(child.children_id)
            tree.extend(a)
        return tree

    def __get_up_category_tree(self, category_id: int) -> List[CategoryOperation]:
        """
        rises up the category tree
        :param category_id: id children category
        :return: list parent category
        """
        category_list = []
        while True:
            category = (
                self.session.query(LevelCategoryModel)
                    .filter(LevelCategoryModel.children_id == category_id)
            )
            category = category.join(CategoryModel,
                                     CategoryModel.id ==
                                     LevelCategoryModel.children_id).first()

            category_id = category.as_dict().get('parent_id')

            if category.as_dict().get('parent_id') is None:
                category_list.append(self.session.query(CategoryModel).filter(
                    CategoryModel.id == category.as_dict().get('children_id')).first())
                break

            category_list.append(self.session.query(CategoryModel).filter(
                CategoryModel.id == category.as_dict().get('children_id')).first())

        return_category_list: List[CategoryOperation] = []
        for item in category_list:
            return_category_list.append(CategoryOperation(id=item.id, name=item.name))
        return return_category_list

