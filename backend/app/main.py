"""
FastAPI Main Application
TaskFlow Backend - GIAIC Hackathon Phase II
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.database import create_db_and_tables
from app.routers import auth, tasks, chat, files, admin

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events - startup and shutdown
    """
    # Startup: Create database tables
    print("Creating database tables...")
    create_db_and_tables()
    print("Database tables created successfully!")

    yield

    # Shutdown
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="TaskFlow API",
    description="Full-Stack Todo Application API - GIAIC Hackathon Phase II by Asif Ali AstolixGen",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for public API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(chat.router)  # Phase III: AI Chat
app.include_router(files.router)  # File Upload
app.include_router(admin.router)  # Admin Panel


@app.get("/")
def read_root():
    """Root endpoint - API information"""
    return {
        "name": "TaskFlow API",
        "version": "2.1.0",
        "author": "Asif Ali AstolixGen",
        "hackathon": "GIAIC Hackathon II",
        "phase": "Phase V+ - Advanced Features + File Upload",
        "docs": "/docs",
        "health": "/api/health",
        "chat": "/api/chat",
        "files": "/api/files",
        "admin": "/api/admin"
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
