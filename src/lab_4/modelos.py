from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr, Field, field_validator


@dataclass(frozen=True, order=True)
class Order:
    order_id: int
    items: List[str] = field(compare=False)
    total: float

    # Un cálculo derivado (Propiedad)
    @property
    def tax(self) -> float:
        return self.total * 0.16

    # Dunder method para representación amigable
    def __str__(self):
        return f"Orden #{self.order_id} | Total: ${self.total:.2f}"


# Pydantic
class OrderIn(BaseModel):
    customer_email: EmailStr
    items: List[str]
    price_per_item: float = Field(gt=0, description="El precio debe ser mayor a 0")

    # Validación personalizada
    @field_validator("items")
    @classmethod
    def check_items_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError("La orden debe tener al menos un item")
        return v


class OrderOut(BaseModel):
    order_id: int
    status: str = "processed"
    total_with_tax: float
    timestamp: datetime = Field(default_factory=datetime.now)
