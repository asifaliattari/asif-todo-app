# REST API Endpoints Specification

**Author**: Asif Ali AstolixGen
**Phase**: Phase II
**Base URL**:
- Development: `http://localhost:8000`
- Production: `https://your-backend.railway.app` or `https://your-backend.onrender.com`

## Authentication

All task endpoints require JWT authentication.

**Header Format**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Unauthorized Response** (401):
```json
{
  "detail": "Not authenticated"
}
```

## Auth Endpoints

### POST /api/auth/signup

Create a new user account.

**Request**:
```json
{
  "name": "Asif Ali AstolixGen",
  "email": "asif@example.com",
  "password": "SecurePassword123"
}
```

**Success Response** (201 Created):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "clx1234567890",
    "name": "Asif Ali AstolixGen",
    "email": "asif@example.com",
    "created_at": "2026-02-10T00:00:00Z"
  }
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input
- `409 Conflict`: Email already registered
- `500 Internal Server Error`: Server error

### POST /api/auth/login

Authenticate existing user.

**Request**:
```json
{
  "email": "asif@example.com",
  "password": "SecurePassword123"
}
```

**Success Response** (200 OK):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "clx1234567890",
    "name": "Asif Ali AstolixGen",
    "email": "asif@example.com",
    "created_at": "2026-02-10T00:00:00Z"
  }
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Invalid credentials
- `500 Internal Server Error`: Server error

## Task Endpoints

### GET /api/tasks

Get all tasks for the authenticated user.

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Query Parameters** (Optional):
- `completed`: Filter by completion status (`true`, `false`, or omit for all)
- `limit`: Max number of tasks to return (default: 100)
- `offset`: Number of tasks to skip (for pagination)

**Success Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "clx1234567890",
      "title": "Complete hackathon project",
      "description": "Finish Phase II implementation",
      "completed": false,
      "created_at": "2026-02-10T10:00:00Z",
      "updated_at": "2026-02-10T10:00:00Z"
    },
    {
      "id": 2,
      "user_id": "clx1234567890",
      "title": "Deploy to Vercel",
      "description": "",
      "completed": true,
      "created_at": "2026-02-09T15:30:00Z",
      "updated_at": "2026-02-10T09:00:00Z"
    }
  ],
  "total": 2
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid token
- `500 Internal Server Error`: Server error

### POST /api/tasks

Create a new task.

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Request**:
```json
{
  "title": "New task title",
  "description": "Optional description"
}
```

**Success Response** (201 Created):
```json
{
  "id": 3,
  "user_id": "clx1234567890",
  "title": "New task title",
  "description": "Optional description",
  "completed": false,
  "created_at": "2026-02-10T12:00:00Z",
  "updated_at": "2026-02-10T12:00:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input (e.g., title missing or too long)
- `401 Unauthorized`: Missing or invalid token
- `500 Internal Server Error`: Server error

**Validation Rules**:
- `title`: Required, 1-200 characters
- `description`: Optional, max 1000 characters

### GET /api/tasks/{id}

Get a specific task by ID.

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Success Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "clx1234567890",
  "title": "Complete hackathon project",
  "description": "Finish Phase II implementation",
  "completed": false,
  "created_at": "2026-02-10T10:00:00Z",
  "updated_at": "2026-02-10T10:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Task belongs to another user
- `404 Not Found`: Task ID doesn't exist
- `500 Internal Server Error`: Server error

### PUT /api/tasks/{id}

Update an existing task.

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Request** (all fields optional, but at least one required):
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true
}
```

**Success Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "clx1234567890",
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true,
  "created_at": "2026-02-10T10:00:00Z",
  "updated_at": "2026-02-10T14:00:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Task belongs to another user
- `404 Not Found`: Task ID doesn't exist
- `500 Internal Server Error`: Server error

### PATCH /api/tasks/{id}/complete

Toggle task completion status.

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Request Body**: None required

**Success Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "clx1234567890",
  "title": "Complete hackathon project",
  "description": "Finish Phase II implementation",
  "completed": true,
  "created_at": "2026-02-10T10:00:00Z",
  "updated_at": "2026-02-10T14:30:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Task belongs to another user
- `404 Not Found`: Task ID doesn't exist
- `500 Internal Server Error`: Server error

### DELETE /api/tasks/{id}

Delete a task permanently.

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Success Response** (204 No Content):
```
(Empty body)
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Task belongs to another user
- `404 Not Found`: Task ID doesn't exist
- `500 Internal Server Error`: Server error

## Additional Endpoints

### GET /api/health

Health check endpoint (no authentication required).

**Success Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2026-02-10T15:00:00Z",
  "version": "1.0.0"
}
```

### GET /docs

FastAPI automatic documentation (Swagger UI).

Access at: `http://localhost:8000/docs`

## Error Response Format

All error responses follow this format:

```json
{
  "detail": "Human-readable error message"
}
```

Or for validation errors:

```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## HTTP Status Codes

- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Authenticated but not authorized (wrong user)
- `404 Not Found`: Resource doesn't exist
- `409 Conflict`: Resource already exists (e.g., email)
- `500 Internal Server Error`: Server-side error

## CORS Configuration

**Allowed Origins**:
- Development: `http://localhost:3000`
- Production: `https://your-app.vercel.app`

**Allowed Methods**: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS`

**Allowed Headers**: `Content-Type`, `Authorization`

## Rate Limiting (Future)

Not implemented in Phase II, but recommended for production:
- 100 requests per minute per IP
- 1000 requests per hour per user

## API Versioning (Future)

Current: No versioning (`/api/...`)
Future: Versioned endpoints (`/api/v1/...`, `/api/v2/...`)

## Example API Calls

### Using curl

**Signup**:
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Asif","email":"asif@test.com","password":"test1234"}'
```

**Get Tasks**:
```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Create Task**:
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"title":"New task","description":"Task details"}'
```

### Using JavaScript (Frontend)

```typescript
// Get tasks
const response = await fetch('http://localhost:8000/api/tasks', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
const data = await response.json();

// Create task
const response = await fetch('http://localhost:8000/api/tasks', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'New task',
    description: 'Optional description'
  })
});
const newTask = await response.json();
```

## Testing

Use FastAPI's built-in Swagger UI for manual testing:
- Navigate to `http://localhost:8000/docs`
- Click "Authorize" button
- Enter JWT token
- Test endpoints interactively

## Summary

This API provides:
- ✅ Secure authentication with JWT
- ✅ Complete CRUD operations for tasks
- ✅ User isolation (can only access own tasks)
- ✅ Input validation
- ✅ Proper error handling
- ✅ RESTful conventions
- ✅ Auto-generated documentation
