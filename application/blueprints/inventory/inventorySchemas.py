from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import validate
from application.extensions import ma
from application.models import Inventory
from ..product.productSchemas import ProductReadSchema
from ..location.locationSchemas import LocationSchema



class InventoryReadSchema(SQLAlchemySchema):
    class Meta:
        model = Inventory

    id = auto_field()
    product = ma.Nested(ProductReadSchema)
    location = ma.Nested(LocationSchema)
    quantity = auto_field()
    reorder_level = auto_field()

class InventoryAdjustSchema(ma.Schema):
    quantity_delta = ma.Integer(required=True)
    note = ma.String()
