from flask import (
    Blueprint,
    request,
    session,
    jsonify
)
from flask.views import MethodView
from marshmallow import ValidationError
from scheme.category import create_category_schema
from services.category import CategoryService, CategoryAlredyExist, CategoryParentIdDoesNotExist
from database import db
import sqlite3

bp = Blueprint('categories', __name__)


class CategoryView(MethodView):
    def post(self):
        """Добавить категорию"""
        user_id = session.get('user_id')
        if user_id is None:
            return jsonify({"answer": "Авторизуйтесь"}), 401
        request_json = request.json
        try:
            category_data = create_category_schema.load(request_json)
        except ValidationError as e:
            return jsonify({"answer": "Ошибка в запросе"}), 400

        try:
            category_service = CategoryService(db.connection, user_id)
            new_category = category_service.add_category(category_data)
            return create_category_schema.dump(new_category), 201
        except CategoryAlredyExist:
            return jsonify({"answer": "Категория существует"}), 400
        except CategoryParentIdDoesNotExist:
            return jsonify({"answer": "Категории с таким parent_id не существует"}), 400


bp.add_url_rule('', view_func=CategoryView.as_view('categories'))

