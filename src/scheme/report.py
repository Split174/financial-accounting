"""
the module contains schemes for validation
:classes:
ReportScheme - validates input data
GetReportScheme - scheme for processing the total amount and data list
ReportOperationScheme - scheme for processing list items
CategoryOperationScheme - scheme for processing the id and name in category
"""
from marshmallow import ValidationError, fields, validates, validates_schema
from scheme.base_scheme import BaseSchema
from entities.report import Report, ReportGet, ReportOperation, CategoryOperation


class ReportScheme(BaseSchema):
    """
    validates input data
    """
    __entity_class__ = Report
    start_date = fields.DateTime(missing=None)
    finish_date = fields.DateTime(missing=None)
    category_name = fields.String(missing=None)
    page = fields.Integer(required=True)
    page_size = fields.Integer(required=True)
    ready_date = fields.String(missing=None)

    @validates('ready_date')
    def validate_ready_date(self, ready_date):
        """
        checks if the requested period exists
        :param ready_date: ready date
        """
        access_date = ('this_week', 'previous_week', 'current_month',
                       'previous_month', 'current_quarter', 'previous_quarter',
                       'this_year', 'last_year', 'all_time')
        if ready_date is not None:
            if ready_date not in access_date:
                raise ValidationError(f'Доступные периоды: {access_date}')

    @validates('page')
    def validate_page(self, page):
        """
        checks if the data is entered correctly
        :param page: page
        """
        if page < 0:
            raise ValidationError('page должно быть положительным числом')

    @validates('page_size')
    def validate_page_size(self, page_size):
        """
        checks if the data is entered correctly
        :param page_size: page size
        """
        if page_size < 0:
            raise ValidationError('page_size должно быть положительным числом')

    @validates_schema
    def validate_date(self, data, **kwargs):
        """
        checks if the date data is entered correctly
        """
        if not ((data['start_date'] is None and data['finish_date'] is None)
                or (data['start_date'] is not None
                    and data['finish_date'] is not None)):
            raise ValidationError('Введите start_date и finish_date')

        if data['start_date'] is not None and data['finish_date'] is not None:
            if data['start_date'] > data['finish_date']:
                raise ValidationError('start_date не должен быть больше '
                                      'finish_date')

        if (data['start_date'] is not None
                and data['finish_date'] is not None
                and data['ready_date'] is not None):
            raise ValidationError('На ввод доступно или временной период'
                                  'или даты на выбор')


class GetReportScheme(BaseSchema):
    """
    scheme for processing the total amount and data list
    """
    __entity_class__ = ReportGet
    result_sum = fields.Decimal(as_string=True, missing=None)
    operation = fields.Nested("ReportOperationScheme", many=True)


class ReportOperationScheme(BaseSchema):
    """
    scheme for processing list items
    """
    __entity_class__ = ReportOperation
    amount = fields.Decimal(as_string=True)
    description = fields.String(missing=None)
    datetime = fields.DateTime()
    category = fields.Nested("CategoryOperationScheme", many=True, missing=None)


class CategoryOperationScheme(BaseSchema):
    """
    scheme for processing the id and name in category
    """
    __entity_class__ = CategoryOperation
    id = fields.Integer()
    name = fields.String()


report_scheme = ReportScheme()
report_get_scheme = GetReportScheme()
