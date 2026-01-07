from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import validate
from application.extensions import ma
from application.models import Role


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)