from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import validate
from application.extensions import ma
from application.models import Inventory
from ..product.productSchemas import ProductReadSchema
from ..location.locationSchemas import LocationSchema



class InventoryReadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        include_relationships = True
inventory_schema = InventoryReadSchema()
inventory_list_schema = InventoryReadSchema(many=True)


class InventoryAdjustSchema(ma.Schema):
    quantity_delta = ma.Integer(required=True)
    note = ma.String()
