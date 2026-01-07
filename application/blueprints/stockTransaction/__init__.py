from flask import Blueprint

stock_transactions_bp = Blueprint("stock_transactions_bp", __name__)

from . import routes