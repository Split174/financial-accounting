from marshmallow import Schema, fields, post_load, validates, ValidationError
from database import db
from models import CategoryModel
from entities.category import CategoryCreate


class CreateCategorySchema(Schema):
    __entity_class__ = CategoryCreate
    id = fields.Integer()
    name = fields.String(required=True)
    parent_id = fields.Integer(load_only=True)
    parent_name = fields.String()
    """@validates('parent_id')
    def validate_parent_id(self, parent_id):
        session = db.connection
        category = session.query(Category).filter(Category.id == parent_id).first()
        if category is None:
            raise ValidationError("Parent category does not exist")"""


create_category_schema = CreateCategorySchema()

