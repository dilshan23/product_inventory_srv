from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import Product, Order, OrderItem, OrderStatus
from fastapi import HTTPException

class LogisticsService:
    @staticmethod
    def create_order(db: Session, items_input: list):
        # Start transaction context
        try:
            new_order = Order(status=OrderStatus.PENDING)
            db.add(new_order)
            db.flush() # Get order ID without committing

            for item in items_input:
                # SELECT ... FOR UPDATE locks the row until commit/rollback
                stmt = select(Product).filter_by(id=item.product_id).with_for_update()
                product = db.execute(stmt).scalar_one_or_none()

                if not product or product.stock < item.quantity:
                    raise HTTPException(status_code=400, detail=f"Inadequate stock for {item.product_id}")

                # Update stock and record historical price
                product.stock -= item.quantity
                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=product.id,
                    quantity=item.quantity,
                    price_at_order=product.price
                )
                db.add(order_item)

            db.commit()
            db.refresh(new_order)
            return new_order
        except Exception as e:
            db.rollback()
            raise e