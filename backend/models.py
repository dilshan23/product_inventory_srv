from datetime import datetime
from enum import Enum
from typing import List
from sqlalchemy import String, Float, Integer, ForeignKey, DateTime, CheckConstraint, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class OrderStatus(str, Enum):
    PENDING = "Pending"
    SHIPPED = "Shipped"
    CANCELLED = "Cancelled"

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    
    __table_args__ = (CheckConstraint("stock >= 0", name="non_negative_stock"),)

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[OrderStatus] = mapped_column(String, default=OrderStatus.PENDING)
    
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    price_at_order: Mapped[float] = mapped_column(Float)

    order: Mapped["Order"] = relationship(back_populates="items")