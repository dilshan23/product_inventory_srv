from sqlalchemy.orm import Session
from database import get_db
from backend.services import LogisticsService
import schemas # Pydantic models

router = APIRouter()

@router.get("/products", response_model=list[schemas.ProductOut])
def list_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Product).offset(skip).limit(limit).all()