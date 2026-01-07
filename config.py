from dotenv import load_dotenv
import os

load_dotenv()

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{os.environ.get('DB_PASSWORD')}@localhost:3306/instock_db'
    DEBUG = True


class TestingConfig:
    pass


class ProductionConfig:
    pass