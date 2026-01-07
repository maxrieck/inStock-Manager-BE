from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import validate
from application.extensions import ma
from application.models import Category


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
