---
title: TaskFlow API
emoji: ✅
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
app_port: 7860
---

# TaskFlow Backend API

FastAPI backend for TaskFlow todo application.

**Created by Asif Ali AstolixGen for GIAIC Hackathon 2026**

## Features

- JWT Authentication
- User signup and login
- Task CRUD operations
- User isolation (each user sees only their own tasks)
- Neon PostgreSQL database
- Automatic API documentation at `/docs`

## Environment Variables

Required:
- `DATABASE_URL` - Neon PostgreSQL connection string
- `SECRET_KEY` - JWT secret key (generate with `openssl rand -base64 32`)

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new account
- `POST /api/auth/login` - Login

### Tasks (Requires Authentication)
- `GET /api/tasks` - Get all user tasks
- `POST /api/tasks` - Create task
- `PUT /api/tasks/{id}` - Update task
- `PATCH /api/tasks/{id}/complete` - Toggle completion
- `DELETE /api/tasks/{id}` - Delete task

## Documentation

Visit `/docs` for interactive Swagger UI documentation.

## Tech Stack

- FastAPI
- SQLModel
- Neon PostgreSQL
- JWT + bcrypt
- Python 3.12
