"""
this module allows get report
:class:
ReportView - gives a report by category
"""
from flask.views import MethodView
from flask import jsonify, request, Blueprint
from marshmallow import ValidationError
from auth_required import auth_required
from database import db
from services.report import ReportService
from scheme.report import report_scheme
from services.report import ReportCategoryError
bp = Blueprint('report', __name__)


class ReportView(MethodView):
    """
    gives a report by category
    """
    @auth_required
    def get(self, user_id):
        """
        gets categories by categories\date
        :param user_id: user id in session
        :return: json with report date
        """
        request_args = request.args
        try:
            report = report_scheme.load(request_args)
        except ValidationError as val_er:
            return jsonify(val_er.messages), 400
        service = ReportService(db.connection, user_id=user_id)
        try:
            return_report = service.get_report(report)
        except ReportCategoryError as rep_err:
            return rep_err.message, 404
        return return_report, 200


bp.add_url_rule('', view_func=ReportView.as_view('report'))
