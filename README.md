# Product & Order Inventory Service

This service manages a product catalog and customer orders using **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. It uses **Alembic** for database version control and is fully containerized with **Docker**.

---

## 🚀 Getting Started

### 1. Prerequisites
* Docker and Docker Compose installed.
* Ensure ports `8000` (API) and `5432` (Database) are not currently in use.

### 2. Launch the Environment
Run this command from the project root (where `docker-compose.yml` is located):

```bash
docker-compose up --builds
```

### 3. Access the Service
Interactive API Docs (Swagger): http://localhost:8000/docs

Alternative Docs (ReDoc): http://localhost:8000/redoc

Health Check: http://localhost:8000/


### 🛠 Database Migrations (Alembic)
The service automatically applies migrations to the latest version (upgrade head) every time the containers start.

Create a New Migration
If you modify backend/models.py (e.g., adding a new table or field), generate a new migration script by running:


```bash

docker exec -it logistics_api alembic revision --autogenerate -m "Describe your changes here"
```
Manually Apply Migrations
If you need to force an upgrade without restarting the container:

Bash

docker exec -it logistics_api alembic upgrade head