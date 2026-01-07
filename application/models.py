from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, UTC
from sqlalchemy import ForeignKey
from decimal import Decimal


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(150), nullable=False, index=True, unique=True)
    password: Mapped[str] = mapped_column(db.String(250), nullable=False)

    is_active: Mapped[bool] = mapped_column(db.Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))

    role_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    role = db.relationship("Role", back_populates="users")


# Sets up Role Based Access Control for User Class
class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50), nullable=False)

    users = db.relationship("User", back_populates="role")


# This focuses on what the item is, does not include location or quanity
class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(db.String(64), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(db.String(150), nullable=False)
    description: Mapped[str] = mapped_column(db.Text)
    price: Mapped[Decimal] = mapped_column(db.Numeric(10, 2), nullable=False)
    active: Mapped[bool] = mapped_column(db.Boolean, default=True, nullable=False)

    category_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    category = db.relationship("Category", back_populates="products")

    inventory = db.relationship("Inventory", back_populates="product", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)

    products = db.relationship("Product", back_populates="category", cascade="all, delete-orphan")


# This includes the location and quanity of product. Product and Location class each
# have a one-to-many relationship with Inventory Class.
class Inventory(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("products.id"))
    location_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("locations.id"))

    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False, default=0)
    reorder_level: Mapped[int] = mapped_column(db.Integer, default=0)

    __table_args__ = (
        db.UniqueConstraint("product_id", "location_id", name="uix_product_location"),
    )

    product = db.relationship("Product", back_populates="inventory")
    location = db.relationship("Location", back_populates="inventory")


class Location(Base):
    __tablename__ = 'locations'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    type: Mapped[str] = mapped_column(db.String(50), nullable=False)
    # this is for a soft delete. 
    is_active: Mapped[bool] = mapped_column(db.Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=lambda: datetime.now(UTC))
    deleted_at: Mapped[datetime] = mapped_column(db.DateTime, default=None, nullable=True)

    inventory = db.relationship("Inventory", back_populates="location")



class StockTransaction(Base):
    __tablename__ = 'stock_transactions'

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    location_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    quantity_delta: Mapped[int] = mapped_column(db.Integer, nullable=False)
    transaction_type: Mapped[str] = mapped_column(db.String(30), name="tx_type", nullable=False)

    created_at: Mapped[datetime] = mapped_column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    note: Mapped[str] = mapped_column(db.Text)

    product = db.relationship('Product')
    location = db.relationship('Location')
    user = db.relationship('User')

