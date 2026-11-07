import uuid
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Numeric, Boolean, UniqueConstraint, CheckConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

def uid(): return str(uuid.uuid4())
class User(Base):
    __tablename__="users"
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=uid)
    email: Mapped[str]=mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str]=mapped_column(String(255))
    role: Mapped[str]=mapped_column(String(32), default="customer")
    active: Mapped[bool]=mapped_column(Boolean, default=True)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
class Category(Base):
    __tablename__="categories"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(120), unique=True)
class Product(Base):
    __tablename__="products"
    id: Mapped[int]=mapped_column(primary_key=True)
    category_id: Mapped[int|None]=mapped_column(ForeignKey("categories.id"))
    name: Mapped[str]=mapped_column(String(200), index=True)
    description: Mapped[str]=mapped_column(Text, default="")
    price: Mapped[float]=mapped_column(Numeric(12,2))
    active: Mapped[bool]=mapped_column(Boolean, default=True)
class Warehouse(Base):
    __tablename__="warehouses"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(120))
class Inventory(Base):
    __tablename__="inventory"
    __table_args__=(UniqueConstraint("product_id","warehouse_id"), CheckConstraint("on_hand >= 0 AND reserved >= 0 AND reserved <= on_hand"))
    id: Mapped[int]=mapped_column(primary_key=True)
    product_id: Mapped[int]=mapped_column(ForeignKey("products.id"), index=True)
    warehouse_id: Mapped[int]=mapped_column(ForeignKey("warehouses.id"))
    on_hand: Mapped[int]=mapped_column(Integer, default=0)
    reserved: Mapped[int]=mapped_column(Integer, default=0)
class Order(Base):
    __tablename__="orders"
    id: Mapped[str]=mapped_column(String(36),primary_key=True,default=uid)
    user_id: Mapped[str]=mapped_column(ForeignKey("users.id"),index=True)
    status: Mapped[str]=mapped_column(String(32),default="CREATED",index=True)
    total: Mapped[float]=mapped_column(Numeric(12,2))
    created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class OrderItem(Base):
    __tablename__="order_items"
    id: Mapped[int]=mapped_column(primary_key=True)
    order_id: Mapped[str]=mapped_column(ForeignKey("orders.id",ondelete="CASCADE"))
    product_id: Mapped[int]=mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int]=mapped_column(Integer)
    unit_price: Mapped[float]=mapped_column(Numeric(12,2))
class OutboxEvent(Base):
    __tablename__="outbox_events"
    id: Mapped[str]=mapped_column(String(36),primary_key=True,default=uid)
    event_type: Mapped[str]=mapped_column(String(100))
    payload: Mapped[str]=mapped_column(Text)
    created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    published_at: Mapped[datetime|None]=mapped_column(DateTime)
