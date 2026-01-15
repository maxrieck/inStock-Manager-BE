from . import stock_transactions_bp
from .transactionSchemas import StockTransactionCreateSchema, StockTransactionReadSchema
from sqlalchemy import select
from flask import request, jsonify, abort
from marshmallow import ValidationError
from application.models import StockTransaction, db
from application.services.inventory_services import InventoryService
from application.utils.utils import token_required
#from application.extensions import limiter, cache


@stock_transactions_bp.route('/', methods=['POST'])
@token_required
def create_transaction(current_user_role, current_user_id):
    data = StockTransactionCreateSchema().load(request.json)

    transaction = InventoryService.adjust_stock(
        product_id=data["product_id"],
        location_id=data['location_id'],
        user_id = current_user_id,
        quantity_delta=data["quantity_delta"],
        tx_type=data["transaction_type"],
        note=data.get("note")
    )

    return StockTransactionReadSchema().dump(transaction), 201