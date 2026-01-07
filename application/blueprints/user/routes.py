from . import users_bp
from .userSchemas import UserCreateSchema, UserReadSchema
from sqlalchemy import select
from flask import request, jsonify, abort
from marshmallow import ValidationError
from application.models import User, db, Role
from werkzeug.security import generate_password_hash
#from application.extensions import limiter, cache
#from application.utils.util import encode_token, token_required


@users_bp.route('/', methods=['POST'])
def create_user():
    try:
        user = UserCreateSchema(session=db.session).load(request.get_json())
    except ValidationError as e:
        return jsonify(e.messages), 400
    user.password = generate_password_hash(user.password)
    query = select(User).where(User.email == user.email)
    existing_user = db.session.execute(query).scalars().all()
    if existing_user:
        return jsonify({"error": "Email already associated with an account"}), 400
    db.session.add(user)
    db.session.commit()
    return jsonify(UserCreateSchema().dump(user)), 201


@users_bp.route('/', methods=['GET'])
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()

    return UserReadSchema(many=True).dump(users)


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.get(User, user_id)

    if user:
        return UserReadSchema().dump(user), 200
    return jsonify({"error": "User not found."}), 404


@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"error": "User not found."}), 404
    try:
        user_data = UserCreateSchema(session=db.session).load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    user.first_name = user_data.first_name
    user.last_name = user_data.last_name
    user.email = user_data.email
    
    db.session.commit()
    return UserCreateSchema().dump(user), 200


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    # if not current_user.is_authenticated or current_user.role.name != 'Admin':
    #     abort(403, description="Admin privileges required.")

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully."}), 200


@users_bp.route('/<int:user_id>/role', methods=['PUT'])
def assign_role(user_id):
    
    # if not current_user.is_authenticated or current_user.role.name != 'Admin':
    #     abort(403, description="Admin privileges required.")

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    role_id = data.get('role_id')
    if not role_id:
        return jsonify({"error": "role_id is required"}), 400

    role = db.session.get(Role, role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404

    user.role_id = role_id
    db.session.commit()
    return jsonify({"message": "Role updated successfully."}), 200