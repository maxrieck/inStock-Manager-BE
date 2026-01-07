from . import products_bp
from .productSchemas import ProductCreateSchema, ProductReadSchema
from sqlalchemy import select
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import Product, db
#from application.extensions import limiter, cache
#from application.utils.util import encode_token, token_required



@products_bp.route('/', methods=['POST'])
def create_product():
    try:
        product_data = ProductCreateSchema(session=db.session).load(request.get_json())
    except ValidationError as e:
        return (jsonify(e.messages)), 400
    query = select(Product).where(Product.sku == product_data.sku)
    existing_product = db.session.execute(query).scalars().all()
    if existing_product:
        return jsonify({"error": "Product with this SKU already exists in inventory."})
    db.session.add(product_data)
    db.session.commit()
    
    return jsonify(ProductCreateSchema().dump(product_data)), 201


@products_bp.route('/', methods=['GET'])
def get_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all()

    return ProductReadSchema(many=True).dump(products)


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = db.session.get(Product, product_id)

    if product:
        return ProductReadSchema().dump(product), 200
    return jsonify({"error": "Product not found."}), 404


@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = db.session.get(Product, product_id)

    # if not current_user.is_authenticated or current_user.role.name != 'Supervisor':
    #     abort(403, description="Admin privileges required.")

    if not product:
        return jsonify({"error": "Product not found."}), 404
    try:
        product_data = ProductCreateSchema(session=db.session).load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.sku = product_data.sku
    product.category_id = product_data.category_id
    
    db.session.commit()
    return ProductCreateSchema().dump(product), 200


@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):

    # if not current_user.is_authenticated or current_user.role.name != 'Supervisor':
    #     abort(403, description="Admin privileges required.")

    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"error":"Product not found."}), 404
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message":f"{product.name} deleted successfully."}), 200