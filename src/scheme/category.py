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
from scheme.base_scheme import BaseSchema
from typing import Any


class CreateCategorySchema(BaseSchema):
    """validating a category and converting it to json"""
    __entity_class__ = Category

    id = fields.Integer()
    name = fields.String(required=True)
    parent_id = fields.Integer(missing=None)


class CategoryChangeSchema(BaseSchema):
    """validating a category and converting it to json"""
    __entity_class__ = Category

    id = fields.Integer()
    name = fields.String(missing=None)
    parent_id = fields.Integer(missing=-1)


class CategoryTreeSchema(BaseSchema):
    """class to convert category tree to json"""
    __entity_class__ = CategoryTree

    id = fields.Integer()
    name = fields.String(required=True)
    children = fields.Nested("CategoryTreeSchema", many=True)


create_category_schema = CreateCategorySchema()
change_category_schema = CategoryChangeSchema()
category_tree_schema = CategoryTreeSchema()
