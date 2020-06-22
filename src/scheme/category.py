"""
The module implements marshmallow schemes for data validation
:classes:
CreateCategorySchema - class for validating a category and converting it to json
CategoryTreeSchema - class to convert category tree to json
"""
from marshmallow import Schema, fields, post_load, validates, ValidationError
from database import db
from models import CategoryModel
from entities.category import Category, CategoryTree
from typing import Any


class CreateCategorySchema(Schema):
    """validating a category and converting it to json"""
    __entity_class__ = Category

    id = fields.Integer()
    name = fields.String(required=True)
    parent_id = fields.Integer(missing=None)

    @post_load
    def make_object(self, data, **kwargs):
        if self.__entity_class__:
            return self.__entity_class__(**data)
        return data


class CategoryTreeSchema(Schema):
    """class to convert category tree to json"""
    __entity_class__ = CategoryTree

    id = fields.Integer()
    name = fields.String(required=True)
    children = fields.Nested("CategoryTreeSchema", many=True)

    @post_load
    def make_object(self, data, **kwargs):
        if self.__entity_class__:
            return self.__entity_class__(**data)
        return data


create_category_schema = CreateCategorySchema()
category_tree_schema = CategoryTreeSchema()
