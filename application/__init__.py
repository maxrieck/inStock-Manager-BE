from flask import Flask
from .extensions import ma
from .models import db
from .blueprints.user import users_bp
from .blueprints.category import categories_bp
from .blueprints.inventory import inventories_bp
from .blueprints.location import locations_bp
from .blueprints.product import products_bp
from .blueprints.stockTransaction import stock_transactions_bp
from .blueprints.roles import roles_bp

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    ma.init_app(app)
    db.init_app(app)

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(inventories_bp, url_prefix='/inventory')
    app.register_blueprint(locations_bp, url_prefix='/locations')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(stock_transactions_bp, url_prefix='/stock_transactions')
    app.register_blueprint(roles_bp, url_prefix='/roles')

    return app