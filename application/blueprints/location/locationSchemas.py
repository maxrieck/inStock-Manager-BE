from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import validate
from application.extensions import ma
from application.models import Location



class LocationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Location
        load_instance = True
    id = auto_field()
    name = auto_field(required=True)
    type = auto_field(required=True)
    is_active = auto_field()
    created_at = auto_field()
    deleted_at = auto_field()
location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)

