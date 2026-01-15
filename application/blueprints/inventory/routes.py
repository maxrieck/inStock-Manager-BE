from . import inventories_bp
from .inventorySchemas import inventory_schema, inventory_list_schema
from sqlalchemy import select
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import Inventory, Location, db
#from application.extensions import limiter, cache
#from application.utils.util import encode_token, token_required


@inventories_bp.route('/', methods=['GET'])
def list_inventory():
    stmt = db.select(Inventory).join(Location).filter(Location.is_active.is_(True))

    product_id = request.args.get("product_id", type=int)
    location_id = request.args.get("location_id", type=int)

    if product_id is not None:
        stmt = stmt.filter(Inventory.product_id == product_id)
    if location_id is not None:
        stmt = stmt.filter(Inventory.location_id == location_id)

    inventory_list = db.session.execute(stmt).scalars().all()
    return inventory_list_schema.dump(inventory_list)


@inventories_bp.route('/product/<int:product_id>', methods=['GET'])
def inventory_by_product(product_id):
    stmt = db.select(Inventory).filter(Inventory.product_id == product_id)
    inventory_list = db.session.execute(stmt).scalars().all()
    
    if not inventory_list:
        return {"message": "No inventory found for this product"}, 404

    return inventory_list_schema.dump(inventory_list)


@inventories_bp.route('/location/<int:location_id>', methods=['GET'])
def inventory_by_location(location_id):
    stmt = db.select(Inventory).filter(Inventory.location_id == location_id)
    inventory_list = db.session.execute(stmt).scalars().all()
    
    if not inventory_list:
        return {"message": "No inventory found for this location"}, 404

    return inventory_list_schema.dump(inventory_list)


@inventories_bp.route('/low-stock', methods=['GET'])
def low_stock():
    stmt = db.select(Inventory).filter(Inventory.quantity <= Inventory.reorder_level)
    inventory_list = db.session.execute(stmt).scalars().all()
    
    return inventory_list_schema.dump(inventory_list)
