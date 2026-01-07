from . import categories_bp
from .categorySchemas import category_schema, categories_schema
from sqlalchemy import select
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import Category, db

#from application.extensions import limiter, cache
#from application.utils.util import encode_token, token_required


@categories_bp.route('/', methods=['POST'])
def create_category():
    try:
        category_data = category_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.message), 400
    query = select(Category).where(Category.name == category_data['name'])
    existing_category = db.session.execute(query).scalars().all()
    if existing_category:
        return jsonify({"error": "Category already exists"}), 400
    new_category = Category(**category_data)
    db.session.add(new_category)
    db.session.commit()
    return category_schema.jsonify(category_data), 201

@categories_bp.route('/', methods=['GET'])
def get_categories():
    query = select(Category)
    categories = db.session.execute(query).scalars().all()

    return categories_schema.jsonify(categories)

@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = db.session.get(Category, category_id)

    if category:
        return category_schema.jsonify(category), 200
    return jsonify({"error": "Category not found."}), 404