from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from backend.services import LogisticsService
from backend.models import Order, OrderStatus
from backend import schemas 

router = APIRouter()

@router.post("/orders", response_model=schemas.OrderOut)
def place_order(order_data: schemas.OrderCreate, db: Session = Depends(get_db)):
    return LogisticsService.create_order(db, order_data.items)

@router.patch("/orders/{order_id}/status")
def update_status(order_id: int, status: OrderStatus, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status == OrderStatus.CANCELLED:
        raise HTTPException(status_code=400, detail="Cannot update status of cancelled order")
        
    order.status = status
    db.commit()
    return {"message": "Status updated"}