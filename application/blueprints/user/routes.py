from . import users_bp
from .userSchemas import UserCreateSchema, UserReadSchema, UserUpdateSchema
from sqlalchemy import select
from flask import request, jsonify, abort
from marshmallow import ValidationError
from application.models import User, db, Role
from werkzeug.security import generate_password_hash, check_password_hash
from application.utils.utils import encode_token, token_required
#from application.extensions import limiter, cache


@users_bp.route('/login', methods=['POST'])
def login():
    try:
        credentials = request.json
        email = credentials['email']
        password = credentials['password']
    except KeyError:
        return jsonify({'messages':'Invalid payload, expecting email and password'}), 400
    
    query = select(User).where(User.email==email)
    user = db.session.execute(query).scalar_one_or_none()

    if user and user.is_active and check_password_hash(user.password, password):
        auth_token = encode_token(user.id, user.role.name)

        response = {
            "status":"success",
            "message":"Successfully logged in",
            "auth_token": auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({'messages':'Invalid email or password'}), 401


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
@token_required
def update_user(current_user_role, user_id, current_user_id):
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"error": "User not found."}), 404
    try:
        user_data = UserUpdateSchema(session=db.session).load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    user.first_name = user_data.first_name
    user.last_name = user_data.last_name
    user.email = user_data.email
    
    db.session.commit()
    return UserUpdateSchema().dump(user), 200


# User deactivate their own account (soft delete)
@users_bp.route('/<int:user_id>/deactivate', methods=['PUT'])
@token_required
def deactivate_user_self(current_user_role, user_id, current_user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.is_active = False
    db.session.commit()
    return jsonify({'message': f"User {user_id} deactivated (soft deleted)."})

# Admin deactivate/reactivate a user
@users_bp.route('/<int:user_id>/active', methods=['PUT'])
@token_required
def set_user_active_status(current_user_role, user_id, current_user_id):
    if current_user_role != 'Admin':
        return jsonify({'error': "Admin privileges required"}), 403
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    is_active = data.get('is_active')
    if is_active is None:
        return jsonify({"error": "is_active field is required (true/false)"}), 400
    user.is_active = bool(is_active)
    db.session.commit()
    return jsonify({"message": f"User {user_id} active status set to {user.is_active}."}), 200


@users_bp.route('/<int:user_id>/role', methods=['PUT'])
@token_required
def assign_role(current_user_role, user_id, current_user_id):
    
    if current_user_role!= 'Admin':
        return jsonify({'error':"Admin privileges required"}), 403

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