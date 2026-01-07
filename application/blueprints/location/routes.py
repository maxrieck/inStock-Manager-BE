from . import locations_bp
from .locationSchemas import location_schema, locations_schema
from sqlalchemy import select
from flask import request, jsonify, abort
from marshmallow import ValidationError
from application.models import Location, db
from datetime import datetime, UTC
#from application.extensions import limiter, cache
#from application.utils.util import encode_token, token_required


@locations_bp.route('/', methods=['POST'])
def create_location():
    try:
        location_data = location_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    query = select(Location).where(Location.name == location_data.name)
    existing_location = db.session.execute(query).scalars().all()
    if existing_location:
        return jsonify({"error": "Location already exists."}), 400
    db.session.add(location_data)
    db.session.commit()

    return location_schema.jsonify(location_data), 201


@locations_bp.route('/', methods=['GET'])
def get_locations():
    query = select(Location)
    locations = db.session.execute(query).scalars().all()

    return locations_schema.jsonify(locations)


@locations_bp.route('/<int:location_id>', methods=['GET'])
def get_location(location_id):
    location = db.session.get(Location, location_id)

    if location:
        return location_schema.jsonify(location), 200
    return jsonify({"error": "Location not found."}), 404


@locations_bp.route('/<int:location_id>', methods=['PUT'])
def update_location(location_id):
    location = db.session.get(Location, location_id)

    # if not current_user.is_authenticated or current_user.role.name != 'Supervisor':
    #     abort(403, description="Admin privileges required.")

    if not location:
        return jsonify({"error": "Location not found."}), 404
    try:
        location_data = location_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    location.name = location_data.name
    location.type = location_data.type
        
    db.session.commit()
    return location_schema.jsonify(location), 200


@locations_bp.route('/<int:location_id>/deactivate', methods=['PUT'])
def deactivate_location(location_id):
    location = db.session.get(Location, location_id)

    # if not current_user.is_authenticated or current_user.role.name != 'Supervisor':
    #     abort(403, description="Admin privileges required.")

    if not location:
        return jsonify({"error": "Location not found."}), 404    
    location.is_active = False
    location.deleted_at = datetime.now(UTC)

    db.session.commit()
    return jsonify({"message": "Location deactivated."}), 200


@locations_bp.route('/<int:location_id>/reactivate', methods=['PUT'])
def reactivate_location(location_id):
    location = db.session.get(Location, location_id)

    # if not current_user.is_authenticated or current_user.role.name != 'Supervisor':
    #     abort(403, description="Admin privileges required.")

    if not location:
        return jsonify({"error": "Location not found."}), 404
    location.is_active = True
    location.deleted_at = None
    db.session.commit()
    return jsonify({"message": "Location reactivated."}), 200