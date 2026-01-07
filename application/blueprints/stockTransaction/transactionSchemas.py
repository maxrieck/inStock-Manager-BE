from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import validate
from application.extensions import ma
from application.models import StockTransaction
from ..product.productSchemas import ProductReadSchema
from ..location.locationSchemas import LocationSchema
from ..user.userSchemas import UserReadSchema



class StockTransactionReadSchema(SQLAlchemySchema):
    class Meta:
        model = StockTransaction

    id = auto_field()
    product = ma.Nested(ProductReadSchema)
    location = ma.Nested(LocationSchema)
    user = ma.Nested(UserReadSchema)
    quantity_delta = auto_field()
    transaction_type = auto_field()
    created_at = auto_field()
    note = auto_field()

class StockTransactionCreateSchema(ma.Schema):
    product_id = ma.Integer(required=True)
    location_id = ma.Integer(required=True)
    quantity_delta = ma.Integer(required=True)
    transaction_type = ma.String(
        required=True,
        validate=validate.OneOf(
            ["IN", "OUT", "ADJUSTMENT", "TRANSFER", "RESERVE", "RELEASE"]
        )
    )
    note = ma.String()

