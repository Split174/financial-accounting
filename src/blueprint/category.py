"""
The module implements routing for categories
:classes:
CategoryView - add category and show all categories
CategoryPatchGetDeleteView - change category, get tree category and delete tree category
"""
from flask import (
    Blueprint,
    request,
    session,
    jsonify
)
from flask.views import MethodView
from marshmallow import ValidationError
from scheme.category import create_category_schema, category_tree_schema
from services.category import CategoryService, CategoryAlredyExist, CategoryIdDoesNotExist
from database import db
from auth_required import auth_required

bp = Blueprint('categories', __name__)


class CategoryView(MethodView):
    """
    the class implements routing of creation and output of all categories
    :methods:
    post - create category
    get - get all tree category
    """
    @auth_required
    def post(self, user_id):
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
        except CategoryIdDoesNotExist:
            return jsonify({"answer": "Категории с таким parent_id не существует"}), 400

    @auth_required
    def get(self, user_id):
        category_service = CategoryService(db.connection, user_id)
        forest = category_service.get_all_tree()
        return jsonify(category_tree_schema.dump(forest, many=True)), 200


class CategoryPatchGetDeleteView(MethodView):
    """
    the class implements routing for editing, receiving and deleting a category
    :methods:
    patch - editing category
    get - get tree category
    delete - del category
    """
    @auth_required
    def patch(self, category_id, user_id):
        request_json = request.json
        request_json["id"] = category_id  # TODO выглядит как костыль
        try:
            category_data = create_category_schema.load(request_json)
        except ValidationError as e:
            return jsonify({"answer": "Ошибка в запросе"}), 400

        try:
            category_service = CategoryService(db.connection, user_id)
            changed_category = category_service.change_category(category_data)
            return create_category_schema.dump(changed_category), 200
        except CategoryAlredyExist:
            return jsonify({"answer": "Данное название занято"}), 400
        except CategoryIdDoesNotExist:
            return jsonify({"answer": "Данной категории не существует"}), 400

    @auth_required
    def get(self, category_id, user_id):
        try:
            category_service = CategoryService(db.connection, user_id)
            tree = category_service.get_category_tree(category_id)
            return category_tree_schema.dump(tree), 200
        except CategoryIdDoesNotExist:
            return jsonify({"answer": "Данной категории не существует"}), 400

    @auth_required
    def delete(self, category_id, user_id):
        try:
            category_service = CategoryService(db.connection, user_id)
            category_service.delete_category(category_id)
            return jsonify({"answer": f"Категория {category_id} удалена"}), 200
        except CategoryIdDoesNotExist:
            return jsonify({"answer": "Данной категории не существует"}), 400


bp.add_url_rule('', view_func=CategoryView.as_view('categories'))
bp.add_url_rule('/<int:category_id>', view_func=CategoryPatchGetDeleteView.as_view('category_patch'))
