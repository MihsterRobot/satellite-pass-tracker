# Satellite Tracker API

Satellite Tracker is a RESTful API built with Django and Django REST Framework that allows users to log and query satellite pass events over ground-based observation locations. It supports full CRUD operations, field-level validation, filtering, and token-based authentication, and is deployed on Railway with a PostgreSQL backend.

**Live API:** https://web-production-753cb.up.railway.app/api/v1/

---

## Tech Stack

- Python 3.12
- Django 6.0
- Django REST Framework
- PostgreSQL
- Docker
- Gunicorn
- Railway

---

## Features

- Full CRUD operations for satellites, locations, and pass events
- Token-based authentication — endpoints are protected and require a valid token
- Field-level validation — coordinates, NORAD ID uniqueness, elevation angle constraints
- Filtering by satellite, location, and date range
- N2YO API integration — automatically fetches and stores predicted pass events for a given satellite and location
- Nested serializers — pass responses include full satellite and location details
- Django admin interface for managing data

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/` | Obtain authentication token |
| GET, POST | `/api/v1/satellites/` | List satellites / Create a satellite |
| GET, PUT, PATCH, DELETE | `/api/v1/satellites/<id>/` | Retrieve / Update / Delete a satellite |
| GET, POST | `/api/v1/locations/` | List locations / Create a location |
| GET, PUT, PATCH, DELETE | `/api/v1/locations/<id>/` | Retrieve / Update / Delete a location |
| GET, POST | `/api/v1/passes/` | List passes / Create a pass |
| GET, PUT, PATCH, DELETE | `/api/v1/passes/<id>/` | Retrieve / Update / Delete a pass |
| POST | `/api/v1/passes/predict/` | Fetch and store predicted passes from N2YO |

List endpoints return paginated results with a default page size of 10. Use `?page=2` to access subsequent pages.

### Filtering Examples

- `GET /api/v1/passes/?satellite=1` — filter passes by satellite
- `GET /api/v1/passes/?start_date=2024-01-01&end_date=2024-12-31` — filter passes by date range
- `GET /api/v1/satellites/?satellite_type=weather` — filter satellites by type

### Authentication

All endpoints except `/api/v1/auth/` require a valid token. To authenticate, first obtain a token:

```
POST /api/v1/auth/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

Then include the token in subsequent requests:

```
Authorization: Token your_token_here
```

---

## Local Setup

### Prerequisites

- Python 3.12
- PostgreSQL
- Docker (optional)

### Standard Setup

1. Clone the repository:

```bash
git clone https://github.com/MihsterRobot/satellite-tracker.git
cd satellite-tracker
```

2. Create a `.env` file in the project root with the following variables:

```
SECRET_KEY=your_secret_key
DB_NAME=satellite_tracker
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DEBUG=True
```

3. Create and activate a virtual environment:

```bash
py -m venv venv
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Apply migrations:

```bash
py manage.py migrate
```

6. Create a superuser:

```bash
py manage.py createsuperuser
```

7. Run the development server:

```bash
py manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/v1/`.

### Docker Setup

1. Create a `.env.docker` file with the same variables as `.env` but set `DB_HOST=db`.

2. Build and run the containers:

```bash
docker-compose up --build
```

3. Apply migrations:

```bash
docker-compose exec web python manage.py migrate
```

4. Create a superuser:

```bash
docker-compose exec web python manage.py createsuperuser
```

The API will be available at `http://127.0.0.1:8000/api/v1/`.
