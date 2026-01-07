from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import validate
from application.extensions import ma
from application.models import Product



class ProductReadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_relationships = True
product_schema = ProductReadSchema()
products_schema = ProductReadSchema(many=True)


class ProductCreateSchema(SQLAlchemySchema):
    class Meta:
        model = Product
        load_instance = True

    sku = auto_field(required=True)
    name = auto_field(required=True)
    description = auto_field()
    price = auto_field(required=True)
    category_id = auto_field(required=True)

