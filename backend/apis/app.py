from fastapi import FastAPI
from backend.apis import products, orders

app = FastAPI()
app.include_router(products.router, prefix="")
app.include_router(orders.router, prefix="")

@app.get("/")
async def read_root():
    return {"status": "running"}