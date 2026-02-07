# Phase II Todo Application - Backend

FastAPI backend with PostgreSQL database and JWT authentication.

## Technology Stack

- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT with Better Auth secret
- **Migrations**: Alembic
- **Testing**: pytest with httpx

## Setup Instructions

### Prerequisites

- Python 3.13+
- uv (Python package manager) or pip
- Neon PostgreSQL database account

### Local Development

1. **Create virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # Or with uv:
   uv pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values:
   # - DATABASE_URL from Neon dashboard
   # - BETTER_AUTH_SECRET (generate with: openssl rand -base64 32)
   # - CORS_ORIGINS with frontend URL
   ```

4. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Start development server**:
   ```bash
   uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access API documentation**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── src/
│   ├── models/          # SQLModel database models
│   │   ├── user.py      # User model
│   │   └── task.py      # Task model
│   ├── services/        # Business logic layer
│   │   ├── user_service.py
│   │   └── task_service.py
│   ├── api/
│   │   ├── routes/      # API endpoints
│   │   │   ├── auth.py  # Authentication routes
│   │   │   └── tasks.py # Task CRUD routes
│   │   ├── middleware/  # Request/response middleware
│   │   │   └── jwt_auth.py
│   │   └── main.py      # FastAPI app initialization
│   ├── db/
│   │   ├── database.py  # Database connection
│   │   └── migrations/  # Alembic migrations
│   └── config.py        # Environment configuration
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── requirements.txt
├── .env.example
└── README.md
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py
```

## Deployment

See main project README for deployment instructions to Railway/Render.

## API Endpoints

- **Authentication**:
  - POST /api/auth/signup - Register new user
  - POST /api/auth/signin - Login user (returns JWT token)
  - POST /api/auth/signout - Logout user

- **Tasks** (JWT required):
  - GET /api/{user_id}/tasks - List all tasks
  - POST /api/{user_id}/tasks - Create task
  - GET /api/{user_id}/tasks/{task_id} - Get task
  - PUT /api/{user_id}/tasks/{task_id} - Update task
  - DELETE /api/{user_id}/tasks/{task_id} - Delete task
  - PATCH /api/{user_id}/tasks/{task_id}/toggle - Toggle completion

All task endpoints validate that the user_id in the URL matches the user_id from the JWT token.
