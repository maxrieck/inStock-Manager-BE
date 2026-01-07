from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import validate
from application.extensions import ma
from application.models import Location



class LocationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Location
        load_instance = True
location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)

