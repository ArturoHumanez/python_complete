from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


# Esquemas Producto
class OrderItemBase(BaseModel):
    product_name: str
    quantity: int = Field(..., gt=0, description="La cantidad debe ser mayor a 0")
    price: float = Field(..., gt=0)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int

    class Config:
        from_attributes = True  # Permite que Pydantic lea modelos de SQLAlchemy


# Esquemas Orden
class OrderBase(BaseModel):
    user_id: int


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True


class OrderUpdate(BaseModel):
    status: Optional[str] = None


# Esquemas user
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
