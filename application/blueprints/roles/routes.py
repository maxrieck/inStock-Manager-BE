from . import roles_bp
from .roleSchemas import role_schema, roles_schema
from sqlalchemy import select
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import Role, db
#from application.extensions import limiter, cache
#from application.utils.util import encode_token, token_required


@roles_bp.route('/', methods=['POST'])
def create_role():
    try:
        role_data = role_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.message), 400
    query = select(Role).where(Role.name == role_data['name'])
    existing_category = db.session.execute(query).scalars().all()
    if existing_category:
        return jsonify({"error": "Role already exists"}), 400
    new_role = Role(**role_data)
    db.session.add(new_role)
    db.session.commit()
    return role_schema.jsonify(role_data), 201

