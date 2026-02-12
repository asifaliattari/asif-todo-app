# Docker Setup Guide - TaskFlow Phase 4

## Prerequisites

- Docker Desktop installed (https://www.docker.com/products/docker-desktop)
- Docker Compose (included with Docker Desktop)
- Git

## Quick Start

### 1. Clone and Navigate
```bash
cd D:\hakathon\asif_todo_app_phase2
```

### 2. Build Docker Images
```bash
docker-compose build
```

### 3. Start Services
```bash
docker-compose up
```

Or run in detached mode (background):
```bash
docker-compose up -d
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 5. Stop Services
```bash
docker-compose down
```

## Detailed Setup

### Environment Variables

The application uses environment variables from `backend/.env`:
- `DATABASE_URL` - Neon PostgreSQL connection string
- `SECRET_KEY` - JWT secret key
- `OPENAI_API_KEY` - OpenAI API key for chatbot
- `SENDGRID_API_KEY` - SendGrid API key for emails
- `SENDER_EMAIL` - Email sender address
- `SENDER_NAME` - Email sender name  
- `ADMIN_EMAIL` - Admin email for notifications

### Build Individual Services

**Backend only:**
```bash
docker-compose build backend
```

**Frontend only:**
```bash
docker-compose build frontend
```

### View Logs

**All services:**
```bash
docker-compose logs -f
```

**Specific service:**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Restart Services

```bash
docker-compose restart
```

**Restart specific service:**
```bash
docker-compose restart backend
```

### Remove Everything

**Stop and remove containers, networks:**
```bash
docker-compose down
```

**Also remove volumes:**
```bash
docker-compose down -v
```

**Also remove images:**
```bash
docker-compose down --rmi all
```

## Docker Commands

### List Running Containers
```bash
docker ps
```

### Execute Commands in Container
```bash
# Backend shell
docker exec -it taskflow-backend /bin/bash

# Frontend shell
docker exec -it taskflow-frontend /bin/sh
```

### View Container Resource Usage
```bash
docker stats
```

### Remove Unused Images
```bash
docker image prune -a
```

## Troubleshooting

### Backend Health Check Failing
- Check `backend/.env` has correct DATABASE_URL
- Ensure Neon PostgreSQL database is accessible
- View logs: `docker-compose logs backend`

### Frontend Can't Connect to Backend
- Verify backend is healthy: `docker ps`
- Check network: `docker network ls`
- Ensure `NEXT_PUBLIC_API_URL` is set correctly

### Port Already in Use
If ports 3000 or 8000 are already in use, modify `docker-compose.yml`:
```yaml
ports:
  - "3001:3000"  # Use different host port
```

### Rebuild After Code Changes
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## Production Deployment

For production, use:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Next Steps (Phase 4)

After Docker Compose works:
1. Install Minikube
2. Create Kubernetes manifests
3. Deploy to local Kubernetes cluster

---

**Created by**: Asif Ali AstolixGen
**Hackathon**: GIAIC Hackathon 2026 - Phase 4
