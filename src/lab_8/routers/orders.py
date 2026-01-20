from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db  # Función que conecta con la DB
from ..dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=schemas.OrderResponse)
def create(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_order = models.Order(user_id=current_user.id)
    db.add(new_order)
    db.flush()

    for item in order.items:
        db_item = models.OrderItem(**item.model_dump(), order_id=new_order.id)
        db.add(db_item)

    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/", response_model=List[schemas.OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    # Solo filtramos las órdenes que pertenecen al ID del token
    return db.query(models.Order).filter(models.Order.user_id == current_user.id).all()


@router.patch("/{order_id}", response_model=schemas.OrderResponse)
def update_order(
    order_id: int,
    order_update: schemas.OrderUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_order = (
        db.query(models.Order)
        .filter(models.Order.id == order_id, models.Order.user_id == current_user.id)
        .first()
    )

    if not db_order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    if order_update.status:
        db_order.status = order_update.status

    db.commit()
    db.refresh(db_order)
    return db_order


@router.delete("/{order_id}", status_code=204)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_order = (
        db.query(models.Order)
        .filter(models.Order.id == order_id, models.Order.user_id == current_user.id)
        .first()
    )

    if not db_order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    db.delete(db_order)
    db.commit()
    return None
