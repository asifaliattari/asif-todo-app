# System Architecture - Phase II

**Author**: Asif Ali AstolixGen
**Phase**: Phase II - Full-Stack Web Application

## Overview

Phase II architecture consists of three main components:
1. **Frontend**: Next.js application (client-side)
2. **Backend**: FastAPI server (REST API)
3. **Database**: Neon PostgreSQL (data persistence)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser)                      │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           Next.js Frontend (Port 3000)                 │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │ │
│  │  │   Pages      │  │  Components  │  │  Better Auth │  │ │
│  │  │  /login      │  │  TaskList    │  │  (JWT)      │  │ │
│  │  │  /signup     │  │  TaskForm    │  │             │  │ │
│  │  │  /dashboard  │  │  TaskItem    │  │             │  │ │
│  │  └──────────────┘  └──────────────┘  └─────────────┘  │ │
│  └────────────┬───────────────────────────────────────────┘ │
│               │ HTTP/HTTPS (REST API)                       │
└───────────────┼─────────────────────────────────────────────┘
                │
                │ JWT Bearer Token
                ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Port 8000)                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  API Routes                                            │ │
│  │  ├── POST /api/auth/signup                            │ │
│  │  ├── POST /api/auth/login                             │ │
│  │  ├── GET  /api/tasks                                  │ │
│  │  ├── POST /api/tasks                                  │ │
│  │  ├── PUT  /api/tasks/{id}                             │ │
│  │  ├── DELETE /api/tasks/{id}                           │ │
│  │  └── PATCH /api/tasks/{id}/complete                   │ │
│  └────────────┬───────────────────────────────────────────┘ │
│               │                                              │
│  ┌────────────▼───────────────────────────────────────────┐ │
│  │  Middleware & Services                                │ │
│  │  ├── JWT Verification                                 │ │
│  │  ├── User Authentication                              │ │
│  │  ├── Task Service (CRUD)                              │ │
│  │  └── Error Handling                                   │ │
│  └────────────┬───────────────────────────────────────────┘ │
│               │                                              │
│  ┌────────────▼───────────────────────────────────────────┐ │
│  │  SQLModel ORM                                         │ │
│  │  ├── User Model                                       │ │
│  │  └── Task Model                                       │ │
│  └────────────┬───────────────────────────────────────────┘ │
└───────────────┼─────────────────────────────────────────────┘
                │
                │ SQL Queries
                ▼
┌─────────────────────────────────────────────────────────────┐
│           Neon Serverless PostgreSQL                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Tables                                                │ │
│  │  ├── users                                             │ │
│  │  │   ├── id (primary key)                              │ │
│  │  │   ├── email (unique)                                │ │
│  │  │   ├── hashed_password                               │ │
│  │  │   └── created_at                                    │ │
│  │  │                                                      │ │
│  │  └── tasks                                             │ │
│  │      ├── id (primary key)                              │ │
│  │      ├── user_id (foreign key → users.id)              │ │
│  │      ├── title                                         │ │
│  │      ├── description                                   │ │
│  │      ├── completed (boolean)                           │ │
│  │      ├── created_at                                    │ │
│  │      └── updated_at                                    │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend (Next.js)

**Responsibilities**:
- Render UI components
- Handle user interactions
- Manage client-side state
- Call backend API with JWT tokens
- Handle Better Auth flows

**Key Technologies**:
- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS
- Better Auth

**Pages**:
- `/login` - User login
- `/signup` - User registration
- `/` - Dashboard with task list (protected)

### Backend (FastAPI)

**Responsibilities**:
- Authenticate users (JWT)
- Validate requests
- Execute business logic
- Interact with database
- Return JSON responses

**Key Technologies**:
- FastAPI
- SQLModel (ORM)
- Pydantic (validation)
- JWT for authentication

**Endpoints**: See `@specs/api/rest-endpoints.md`

### Database (Neon PostgreSQL)

**Responsibilities**:
- Store user accounts
- Store tasks
- Maintain data integrity
- Handle queries efficiently

**Schema**: See `@specs/database/schema.md`

## Data Flow

### User Signup Flow
```
1. User fills signup form (Frontend)
2. POST /api/auth/signup → Backend
3. Backend hashes password
4. Backend creates user in DB
5. Backend returns JWT token
6. Frontend stores token
7. Frontend redirects to dashboard
```

### User Login Flow
```
1. User enters credentials (Frontend)
2. POST /api/auth/login → Backend
3. Backend verifies password
4. Backend generates JWT token
5. Backend returns token
6. Frontend stores token
7. Frontend redirects to dashboard
```

### Create Task Flow
```
1. User submits task form (Frontend)
2. POST /api/tasks with JWT → Backend
3. Backend verifies JWT token
4. Backend extracts user_id from token
5. Backend creates task in DB with user_id
6. Backend returns created task
7. Frontend adds task to UI
```

### Get Tasks Flow
```
1. Dashboard loads (Frontend)
2. GET /api/tasks with JWT → Backend
3. Backend verifies JWT token
4. Backend extracts user_id
5. Backend queries tasks WHERE user_id = X
6. Backend returns task array
7. Frontend displays tasks
```

## Security Architecture

### Authentication Flow (Better Auth + JWT)

```
┌─────────────┐                    ┌─────────────┐
│  Frontend   │                    │   Backend   │
│  (Next.js)  │                    │  (FastAPI)  │
└──────┬──────┘                    └──────┬──────┘
       │                                  │
       │  1. Login Request                │
       ├─────────────────────────────────>│
       │     POST /api/auth/login         │
       │     { email, password }          │
       │                                  │
       │                          2. Verify Credentials
       │                             (bcrypt hash)
       │                                  │
       │  3. JWT Token Response           │
       │<─────────────────────────────────┤
       │     { token, user }              │
       │                                  │
  4. Store Token                          │
     in localStorage                      │
       │                                  │
       │  5. API Request with Token       │
       ├─────────────────────────────────>│
       │     GET /api/tasks               │
       │     Authorization: Bearer <JWT>  │
       │                                  │
       │                          6. Verify JWT
       │                             Extract user_id
       │                             Query database
       │                                  │
       │  7. Filtered Response            │
       │<─────────────────────────────────┤
       │     [user's tasks only]          │
       │                                  │
```

### JWT Token Structure
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```

### Security Features

1. **Password Hashing**: bcrypt with salt
2. **JWT Tokens**: Secure, stateless authentication
3. **HTTPS**: All communication encrypted (in production)
4. **CORS**: Configured for frontend origin only
5. **Input Validation**: Pydantic models validate all inputs
6. **SQL Injection Prevention**: SQLModel ORM with parameterized queries
7. **User Isolation**: Each user sees only their own data

## Deployment Architecture

### Development
```
Frontend: localhost:3000
Backend: localhost:8000
Database: Neon (cloud)
```

### Production
```
Frontend: Vercel (vercel.app)
Backend: Railway/Render (.railway.app / .onrender.com)
Database: Neon (cloud)
```

## Performance Considerations

1. **Database Indexing**: Index on user_id for fast task queries
2. **Connection Pooling**: Neon handles connections efficiently
3. **JWT Caching**: Frontend caches token, reducing auth requests
4. **API Response Size**: Only return necessary fields
5. **Frontend Code Splitting**: Next.js automatic code splitting

## Scalability Path

**Current (Phase II)**:
- Single frontend instance (Vercel auto-scales)
- Single backend instance
- Serverless database (Neon auto-scales)

**Future (Phase V)**:
- Multiple backend instances (Kubernetes)
- Load balancer
- Kafka for async processing
- Dapr for service mesh

## Error Handling

### Frontend
- Display user-friendly error messages
- Redirect to login on 401 Unauthorized
- Show validation errors on forms

### Backend
- Return proper HTTP status codes
- Include error messages in JSON response
- Log errors for debugging
- Handle database exceptions gracefully

## Monitoring & Logging

**Development**:
- Console logs
- FastAPI automatic API docs (/docs)

**Production**:
- Vercel analytics (frontend)
- Railway/Render logs (backend)
- Database monitoring (Neon dashboard)

## API Versioning

Current: `/api/` endpoints (no version)
Future: `/api/v1/`, `/api/v2/` for backward compatibility

## Summary

This architecture provides:
- ✅ Clear separation of concerns
- ✅ Secure authentication
- ✅ User data isolation
- ✅ Scalable foundation
- ✅ Easy to test and debug
- ✅ Ready for Phase III (AI Chatbot)
