# TaskFlow - Project Overview

**Author**: Asif Ali AstolixGen
**Hackathon**: GIAIC Hackathon II
**Phase**: Phase II - Full-Stack Web Application

## Purpose

A todo application that evolves from console app to cloud-native AI chatbot, demonstrating mastery of spec-driven development and modern cloud technologies.

## Vision

Build a production-grade task management system that:
- Helps users organize their daily tasks efficiently
- Provides intelligent AI assistance for task management
- Scales from personal use to team collaboration
- Demonstrates modern full-stack development practices

## Current Phase: Phase II

**Goal**: Transform the console app into a modern multi-user web application with persistent storage.

**Status**: In Progress

## Tech Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth
- **Deployment**: Vercel

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.13+
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Deployment**: Railway or Render

### Development Tools
- **Spec Management**: Spec-Kit Plus methodology
- **AI Assistant**: Claude Code
- **Package Manager**: npm (frontend), uv (backend)

## Feature Levels

### Basic Level (Phase II Requirements)
- [x] Add Task – Create new todo items
- [x] Delete Task – Remove tasks from the list
- [x] Update Task – Modify existing task details
- [x] View Task List – Display all tasks
- [x] Mark as Complete – Toggle task completion status

### Intermediate Level (Phase V)
- [ ] Priorities & Tags – Assign levels and categories
- [ ] Search & Filter – Search and filter capabilities
- [ ] Sort Tasks – Multiple sort options

### Advanced Level (Phase V)
- [ ] Recurring Tasks – Auto-reschedule repeating tasks
- [ ] Due Dates & Reminders – Deadlines and notifications

## User Stories (Phase II)

1. **As a new user**, I can sign up with email and password
2. **As a registered user**, I can log in to access my tasks
3. **As a logged-in user**, I can create new tasks
4. **As a logged-in user**, I can view all my tasks
5. **As a logged-in user**, I can update my task details
6. **As a logged-in user**, I can delete my tasks
7. **As a logged-in user**, I can mark tasks as complete/incomplete
8. **As a user**, I only see my own tasks (data isolation)

## Architecture Principles

1. **Separation of Concerns**: Frontend and backend are separate services
2. **API-First**: Backend exposes RESTful API
3. **Stateless**: Backend is stateless, state stored in database
4. **Authentication**: JWT tokens for secure API access
5. **User Isolation**: Each user's data is completely isolated
6. **Responsive Design**: Works on desktop, tablet, and mobile

## Success Criteria

- [ ] All Basic Level features work correctly
- [ ] User authentication is secure (Better Auth + JWT)
- [ ] API endpoints follow REST conventions
- [ ] Frontend is responsive and user-friendly
- [ ] Database schema is properly normalized
- [ ] Code is generated via spec-driven development
- [ ] Both frontend and backend are deployed
- [ ] Demo video (< 90 seconds) showcases all features

## Next Phases Preview

- **Phase III**: Add AI Chatbot with MCP Server
- **Phase IV**: Deploy to local Kubernetes (Minikube)
- **Phase V**: Cloud deployment with Kafka and Dapr

## References

- Hackathon Document: `Hackathon II - Todo Spec-Driven Development.docx`
- Architecture: `@specs/architecture.md`
- Features: `@specs/features/`
- API: `@specs/api/`
- Database: `@specs/database/`
