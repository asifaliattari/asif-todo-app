# 🎬 Docker Demonstration Guide
**TaskFlow - Phase 4 Complete**
**Created for GIAIC Hackathon 2026**

## 🎯 What's Running

Your TaskFlow application is **LIVE on Docker** with:
- ✅ **Backend API**: FastAPI + PostgreSQL
- ✅ **Frontend**: Next.js React App
- ✅ **AI Chatbot**: OpenAI GPT-4o-mini
- ✅ **Email Scheduler**: Background task reminders
- ✅ **Health Checks**: Automatic container monitoring
- ✅ **Network**: Isolated Docker bridge network

---

## 📊 Live Container Status

```bash
docker ps
```

**Output:**
```
NAME                STATUS                   PORTS
taskflow-backend    Up (healthy)             0.0.0.0:8000->8000/tcp
taskflow-frontend   Up                       0.0.0.0:3000->3000/tcp
```

---

## 🚀 Quick Demo Commands (For Video)

### 1. Show Running Containers
```bash
docker ps
```
*Shows both containers running with health status*

### 2. Show Container Logs
```bash
# Backend logs (database, scheduler, API requests)
docker logs taskflow-backend --tail 20

# Frontend logs (Next.js server)
docker logs taskflow-frontend --tail 20
```

### 3. Check Backend Health
```bash
curl http://localhost:8000/api/health
```
*Returns: {"status":"healthy","timestamp":"...","version":"1.0.0"}*

### 4. Check Database Health
```bash
curl http://localhost:8000/api/health/db
```
*Shows database connection status*

### 5. Access the Application

**Frontend**: http://localhost:3000
**Backend API Docs**: http://localhost:8000/docs
**Backend Health**: http://localhost:8000/api/health

### 6. Show Docker Images
```bash
docker images | grep taskflow
```
*Shows both built images with sizes*

### 7. Show Docker Network
```bash
docker network ls | grep taskflow
docker network inspect asif_todo_app_phase2_taskflow-network
```
*Shows isolated network configuration*

### 8. Resource Usage
```bash
docker stats --no-stream
```
*Shows CPU, memory, network usage*

---

## 🎥 Video Recording Script

### **Introduction (30 seconds)**
1. Open terminal
2. Show `docker ps` - containers running
3. Open browser to http://localhost:3000
4. Show TaskFlow dashboard

### **Backend Demonstration (1 minute)**
1. Open http://localhost:8000/docs (Swagger UI)
2. Show API endpoints:
   - `/api/auth/signup`
   - `/api/auth/login`
   - `/api/tasks` (CRUD operations)
   - `/api/chat` (AI chatbot)
   - `/api/health` (health checks)
3. Test health endpoint in terminal:
   ```bash
   curl http://localhost:8000/api/health
   ```

### **Frontend Demonstration (2 minutes)**
1. Open http://localhost:3000
2. **Signup**: Create new account
3. **Dashboard**: Show features
   - Task statistics
   - Progress chart
   - Task filters
   - Beautiful task cards with priorities
4. **Create Task**:
   - Add title, description
   - Set priority (high/medium/low)
   - Add tags
   - Set due date & time
   - Set reminder alert
   - Mark as recurring
5. **Task Management**:
   - Click task → View in modal
   - Edit task directly in modal
   - Mark complete/incomplete
   - Delete task
6. **AI Chatbot**:
   - Click chat icon (bottom right)
   - Ask "Show my pending tasks"
   - Create task via chatbot
7. **Mobile Responsive**: Resize browser window

### **Docker Features (1 minute)**
1. Show container logs:
   ```bash
   docker logs taskflow-backend --tail 20 -f
   ```
2. Show health check working:
   ```bash
   docker inspect taskflow-backend | grep -A 5 Health
   ```
3. Show resource usage:
   ```bash
   docker stats --no-stream
   ```
4. Show network isolation:
   ```bash
   docker network inspect asif_todo_app_phase2_taskflow-network
   ```

### **Stop & Restart (30 seconds)**
1. Stop containers:
   ```bash
   docker-compose down
   ```
   *Show containers stopping gracefully*

2. Restart:
   ```bash
   docker-compose up -d
   ```
   *Show containers starting with health checks*

3. Verify:
   ```bash
   docker ps
   ```
   *Show healthy status*

---

## 📦 Docker Architecture Highlights

### Multi-Stage Builds
- **Backend**: Python 3.13-slim, optimized with pip cache
- **Frontend**: Node 18-alpine, production build with standalone output

### Health Checks
- **Backend**: HTTP check on `/api/health` every 30s
- **Frontend**: Depends on backend being healthy before starting

### Security
- **Non-root users**: Both containers run as unprivileged users
- **Network isolation**: Containers communicate via bridge network
- **Environment variables**: Sensitive data in .env (git-ignored)

### Optimizations
- **Build cache**: Layers cached for faster rebuilds
- **.dockerignore**: Excludes node_modules, .next, __pycache__
- **Standalone mode**: Next.js minimal production bundle

---

## 🔧 Container Management

### View Logs (Real-time)
```bash
docker-compose logs -f
```

### Restart Services
```bash
docker-compose restart
```

### Stop Containers
```bash
docker-compose stop
```

### Remove Containers
```bash
docker-compose down
```

### Rebuild Images
```bash
docker-compose build --no-cache
```

### Start Fresh
```bash
docker-compose down -v  # Remove volumes too
docker-compose up -d --build
```

---

## 📊 Image Details

### Backend Image
- **Size**: 392 MB (compressed: 91.8 MB)
- **Base**: python:3.13-slim
- **Features**:
  - FastAPI + Uvicorn
  - SQLModel + PostgreSQL driver
  - OpenAI SDK
  - SendGrid email
  - APScheduler for reminders
  - Health check with curl

### Frontend Image
- **Size**: 289 MB (compressed: 69.4 MB)
- **Base**: node:18-alpine
- **Features**:
  - Next.js 15.5.12 production build
  - React 19
  - Tailwind CSS
  - Standalone output (minimal size)
  - Non-root user (nextjs:nodejs)

---

## 🌐 Network Architecture

```
┌─────────────────────────────────────────┐
│   Docker Bridge Network                 │
│   (asif_todo_app_phase2_taskflow-network)│
│                                          │
│  ┌──────────────────┐  ┌──────────────┐ │
│  │ taskflow-backend │  │ taskflow-    │ │
│  │                  │  │ frontend     │ │
│  │ Port: 8000       │  │ Port: 3000   │ │
│  │ Health: ✓        │  │ Depends: ↑   │ │
│  │                  │  │              │ │
│  │ FastAPI + DB     │  │ Next.js      │ │
│  └──────────────────┘  └──────────────┘ │
│          ↓                      ↓        │
│    0.0.0.0:8000           0.0.0.0:3000   │
└─────────────────────────────────────────┘
           ↓                      ↓
    API Requests           Web Browser
```

---

## 🎯 Demo Talking Points

### For Video Narration:

1. **"Full-stack application running in Docker containers"**
   - Show `docker ps`

2. **"Isolated network with health checks"**
   - Explain backend health monitoring
   - Show frontend waits for backend

3. **"Production-ready with multi-stage builds"**
   - Mention optimized image sizes
   - Security with non-root users

4. **"Complete task management with AI chatbot"**
   - Demo creating tasks
   - Show AI assistant responding

5. **"Email notifications and recurring tasks"**
   - Show reminder system
   - Mention background scheduler

6. **"Deployed on Neon PostgreSQL"**
   - Serverless database
   - Production-ready persistence

---

## 📝 Quick Reference

### Environment Variables
- `DATABASE_URL`: Neon PostgreSQL connection
- `SECRET_KEY`: JWT authentication secret
- `OPENAI_API_KEY`: AI chatbot integration
- `SENDGRID_API_KEY`: Email notifications (optional)

### Ports
- **3000**: Frontend (Next.js)
- **8000**: Backend (FastAPI)

### Container Names
- `taskflow-backend`
- `taskflow-frontend`

### Network
- `asif_todo_app_phase2_taskflow-network`

---

## ✅ Pre-Recording Checklist

- [ ] Both containers running (`docker ps`)
- [ ] Backend healthy (`curl http://localhost:8000/api/health`)
- [ ] Frontend accessible (`http://localhost:3000`)
- [ ] Create test account for demo
- [ ] Prepare sample tasks with different priorities
- [ ] Test AI chatbot with sample questions
- [ ] Clear browser console for clean demo
- [ ] Set browser zoom to 100%
- [ ] Close unnecessary browser tabs
- [ ] Prepare terminal with commands ready

---

## 🎬 Recording Ready!

Your Docker setup is **complete** and **production-ready**. All features are working:

- ✅ User authentication
- ✅ Task CRUD operations
- ✅ AI chatbot with GPT-4o-mini
- ✅ Email reminders (backend ready, add SendGrid key to enable)
- ✅ Recurring tasks
- ✅ File uploads and permissions
- ✅ Admin panel
- ✅ Real-time updates
- ✅ Mobile responsive design
- ✅ Docker containerization
- ✅ Health monitoring
- ✅ Production optimizations

**Open http://localhost:3000 and start recording!** 🎥

---

*Created by Asif Ali AstolixGen for GIAIC Hackathon 2026 - Phase 4*
