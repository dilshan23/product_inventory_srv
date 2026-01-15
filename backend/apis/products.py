from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import get_db
from backend.models import Product 
from backend import schemas 

router = APIRouter()

@router.get("/products", response_model=list[schemas.ProductOut])
def list_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Product).offset(skip).limit(limit).all()

@router.post("/products", response_model=schemas.ProductOut, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    # 1. Create the database model instance
    db_product = Product(
        name=product.name,
        price=product.price,
        stock=product.stock
        # Add description here if it's in your Model, 
        # but it's not in your ProductBase schema above!
    )
    
    # 2. Save to Postgres
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product