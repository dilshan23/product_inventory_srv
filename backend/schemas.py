from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from backend.models import OrderStatus

# --- Product Schemas ---

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0) 

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# --- Order Item Schemas ---

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderItemOut(OrderItemBase):
    id: int
    price_at_order: float # Historical price tracking

    model_config = ConfigDict(from_attributes=True)

# --- Order Schemas ---

class OrderCreate(BaseModel):
    items: List[OrderItemBase]

class OrderOut(BaseModel):
    id: int
    created_at: datetime
    status: OrderStatus
    items: List[OrderItemOut]
    
    model_config = ConfigDict(from_attributes=True)