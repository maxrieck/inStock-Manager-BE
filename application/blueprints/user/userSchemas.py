from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import validate
from application.extensions import ma
from application.models import User


class UserCreateSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    first_name = auto_field(required=True)
    last_name = auto_field(required=True)
    email = auto_field(required=True)
    password = ma.String(load_only=True, required=True)
    role_id = auto_field(required=True)

class UserReadSchema(SQLAlchemySchema):
    class Meta:
        model = User

    id = auto_field()
    first_name = auto_field()
    last_name = auto_field()
    email = auto_field()
    is_active = auto_field()
    created_at = auto_field()
    role = ma.Nested("RoleSchema")

    
