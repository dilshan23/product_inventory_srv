# product_inventory_srv
### This service will manage product and orders service

## Start backend service-Run in root directory backend
docker-compose up --build api


## To Add a Product

curl -X POST http://localhost:8000/products/ \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Heavy Duty Pallet",
           "description": "Industrial grade wooden pallet",
           "price": 25.50,
           "stock": 100
         }'