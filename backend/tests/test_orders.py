import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.apis.app import app
from backend.apis.database import Base, get_db
from backend.models import Product

# --- Setup Test Database ---
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/logistics_db_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# --- The Tests ---

def test_create_order_success():
    # 1. Create a product first
    product_data = {"name": "Test Item", "price": 100.0, "stock": 10}
    p_resp = client.post("/products", json=product_data)
    product_id = p_resp.json()["id"]

    # 2. Place an order
    order_data = {"items": [{"product_id": product_id, "quantity": 2}]}
    response = client.post("/orders", json=order_data)

    # 3. Assertions
    assert response.status_code == 201
    assert response.json()["status"] == "PENDING"
    
    # 4. Verify stock was reduced
    check_p = client.get("/products")
    # Find our product in the list
    product = next(p for p in check_p.json() if p["id"] == product_id)
    assert product["stock"] == 8


def test_create_order_insufficient_stock():
    # 1. Create a product with low stock
    product_data = {"name": "Low Stock Item", "price": 50.0, "stock": 3}
    p_resp = client.post("/products", json=product_data)
    product_id = p_resp.json()["id"]

    # 2. Try to order more than available
    order_data = {"items": [{"product_id": product_id, "quantity": 10}]}
    response = client.post("/orders", json=order_data)

    # 3. Assertions
    assert response.status_code == 400
    assert "Inadequate stock" in response.json()["detail"]
    
    # 4. Verify stock was NOT touched (Atomicity check)
    check_p = client.get("/products")
    product = next(p for p in check_p.json() if p["id"] == product_id)
    assert product["stock"] == 3