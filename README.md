# Django Marketplace API

Backend API for a marketplace platform built with Django REST Framework.

Project status: active development (pre-production stage).

---

## Project Status

The project is currently in active development and is not production-ready yet.

Current stage:
- authentication and authorization
- notifications
- catalog domain models
- project infrastructure and architecture

Planned before production:
- catalog business logic
- inventory domain
- cart system
- order management
- payment integration
- production infrastructure
- CI/CD
- monitoring and logging

The project is currently focused on completing domain-level implementation before production deployment.

---

## Tech Stack

- Python 3.14
- Django 6
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- JWT Authentication
- DRF Spectacular (OpenAPI)
- Pytest
- Ruff
- Black
- Mypy

---

## Features

Current features:
- JWT authentication
- custom user authentication flow
- notifications system
- catalog domain models
- OpenAPI documentation
- environment-based configuration
- Redis integration
- Celery integration

Planned features:
- product management
- attributes system
- inventory management
- cart system
- order processing
- payment system
- reviews & ratings
- search & filtering
- production hardening
- docker
- deploy
---

## Installation

### 1. Clone repository

```bash
git clone <repository-url>
cd Django-Marketplace-API
```

### 2. Create virtual environment
```bash
python -m venv .venv
```
Activate virtual environment:
- Linux/macOS:
    ```bash
    source .venv/bin/activate
    ```
- Windows:
    ```bash
    .venv\Scripts\activate
    ```

### 3. Install dependencies

- Development:
    ```bash
    pip install -r requirements/development.txt
    ```

- Production:
    ```bash
    pip install -r requirements/production.txt
    ```
---
## Environment Variables
Create .env file in project root.

Example:
```env
SECRET_KEY=your-secret-key

DEBUG=False

ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=marketplaceapi_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True

EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```
---
## Database Setup

- Create PostgreSQL database:
    ```postgres-psql
    CREATE DATABASE db_name;
    ```

- Run migrations:
    ```bash
    python manage.py migrate
    ```

- Create superuser:
    ```bash
    python manage.py createsuperuser
    ```
---
## Running Project
Run development server:
```bash
python manage.py runserver
```

## Running Celery

- Worker:
    ```bash
    celery -A core worker -l info
    ```
- Beat:
    ```bash
    celery -A core beat -l info
    ```
---
## API Documentation
OpenAPI schema:
- /api/schema/

Swagger UI:
- /api/schema/swagger-ui/

ReDoc:
- /api/schema/redoc/

## Testing

Run tests:
```bash
pytest
```
---

## Pre-commit

Install hooks:
```bash
pre-commit install
```

Run hooks manually:
```bash
pre-commit run --all-files
```
---
## Project Architecture

Current architecture focuses on:
- domain separation
- service-oriented business logic
- scalable catalog structure
- environment isolation
- asynchronous task processing

---

## Production Goals

Planned production infrastructure:
- Docker
- Nginx
- Gunicorn
- CI/CD pipeline
- monitoring
- centralized logging
- production-grade security hardening
---

## License

This project is currently for educational and portfolio purposes.