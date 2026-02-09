# Backend Guidelines - TaskFlow API

**Author**: Asif Ali AstolixGen
**Phase**: Phase II
**Framework**: FastAPI + SQLModel

## Overview

This is the backend API for TaskFlow. It provides RESTful endpoints for user authentication and task management.

## Stack

- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL database ORM (combines SQLAlchemy + Pydantic)
- **Neon PostgreSQL** - Serverless database
- **JWT** - JSON Web Tokens for authentication
- **bcrypt** - Password hashing

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app + CORS + lifespan
│   ├── database.py          # Database connection
│   ├── auth.py              # JWT utilities + password hashing
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model + schemas
│   │   └── task.py          # Task model + schemas
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # POST /api/auth/signup, /login
│       └── tasks.py         # CRUD endpoints for tasks
├── pyproject.toml           # UV project config
├── requirements.txt         # Pip dependencies
├── .env                     # Environment variables (git-ignored)
├── .env.example             # Environment template
└── CLAUDE.md                # This file
```

## Setup Instructions

### 1. Install Dependencies

Using UV (recommended):
```bash
cd backend
uv sync
```

Using pip:
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` and set:
```
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
BETTER_AUTH_SECRET=<generate with: openssl rand -base64 32>
FRONTEND_URL=http://localhost:3000
```

### 3. Run Server

```bash
uv run uvicorn app.main:app --reload --port 8000
```

Or:
```bash
python app/main.py
```

Server runs at: `http://localhost:8000`

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database

### Neon Setup

1. Sign up at https://neon.tech
2. Create new project
3. Copy connection string
4. Add to `.env` as `DATABASE_URL`

### Auto-Migration

Tables are created automatically on startup via `create_db_and_tables()` in `app/main.py` lifespan event.

### Models

- **User**: `app/models/user.py`
- **Task**: `app/models/task.py`

See `@specs/database/schema.md` for complete schema.

## API Endpoints

See `@specs/api/rest-endpoints.md` for complete API documentation.

### Authentication
- `POST /api/auth/signup` - Create account
- `POST /api/auth/login` - Login

### Tasks (Requires JWT)
- `GET /api/tasks` - List user's tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks/{id}` - Get task
- `PUT /api/tasks/{id}` - Update task
- `PATCH /api/tasks/{id}/complete` - Toggle completion
- `DELETE /api/tasks/{id}` - Delete task

### Utility
- `GET /` - API info
- `GET /api/health` - Health check

## Authentication Flow

1. User signs up or logs in via `/api/auth/signup` or `/api/auth/login`
2. Backend returns JWT token
3. Frontend includes token in all requests: `Authorization: Bearer <token>`
4. Backend middleware (`get_current_user_id`) verifies token and extracts user_id
5. Endpoints filter data by user_id (user isolation)

## Key Code Patterns

### Dependency Injection

```python
from fastapi import Depends
from app.database import get_session
from app.auth import get_current_user_id

@router.get("/api/tasks")
def get_tasks(
    session: Session = Depends(get_session),      # DB session
    user_id: str = Depends(get_current_user_id)  # Authenticated user
):
    # ...
```

### User Isolation

**Always filter by user_id**:
```python
statement = select(Task).where(Task.user_id == user_id)
```

### Error Handling

```python
from fastapi import HTTPException, status

# Not found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Task not found"
)

# Unauthorized
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials"
)

# Forbidden (wrong user)
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not authorized"
)
```

## Testing

### Manual Testing

Use Swagger UI at `/docs`:
1. Test signup/login
2. Click "Authorize" button
3. Paste JWT token
4. Test task endpoints

### Automated Testing (Future)

```bash
pytest
```

## Deployment

### Railway

1. Sign up at https://railway.app
2. Create new project from GitHub
3. Add service → Select backend folder
4. Set environment variables
5. Deploy

### Render

1. Sign up at https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Root directory: `backend`
5. Build command: `pip install -r requirements.txt`
6. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables
8. Deploy

## Common Issues

### Database Connection Error

- Check `DATABASE_URL` in `.env`
- Ensure Neon project is active
- Verify SSL mode: `?sslmode=require`

### JWT Errors

- Ensure `BETTER_AUTH_SECRET` is set
- Same secret in frontend and backend
- Token must be in `Authorization: Bearer <token>` header

### CORS Errors

- Check `FRONTEND_URL` in `.env`
- Update `allow_origins` in `app/main.py` if needed

## Best Practices

1. **Always use SQLModel** for database operations (prevents SQL injection)
2. **Verify ownership** before modifying tasks
3. **Hash passwords** with bcrypt (never store plaintext)
4. **Validate inputs** with Pydantic models
5. **Return proper HTTP status codes**
6. **Log errors** for debugging

## Security Checklist

- [x] Passwords hashed with bcrypt
- [x] JWT tokens signed with secret
- [x] User isolation (filter by user_id)
- [x] Input validation (Pydantic)
- [x] SQL injection prevention (SQLModel ORM)
- [x] CORS configured for frontend only
- [x] HTTPS in production (handled by Railway/Render)

## References

- Specifications: `@specs/`
- API Docs: `@specs/api/rest-endpoints.md`
- Database Schema: `@specs/database/schema.md`
- Features: `@specs/features/`

---

**For implementation questions, always reference the specs first!**
