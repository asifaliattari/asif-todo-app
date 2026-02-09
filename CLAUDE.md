# TaskFlow - GIAIC Hackathon II - Phase II

**Created by Asif Ali AstolixGen**

## Project Overview

This is a monorepo using **Spec-Kit Plus** methodology for spec-driven development with Claude Code.

This project is part of GIAIC Hackathon II: "The Evolution of Todo – Mastering Spec-Driven Development & Cloud Native AI"

## Current Phase: Phase II - Full-Stack Web Application

Transform the console app into a modern multi-user web application with persistent storage.

## Spec-Kit Plus Structure

Specifications are organized in `/specs`:
- `/specs/overview.md` - Project overview and goals
- `/specs/architecture.md` - System architecture and design
- `/specs/features/` - Feature specifications (what to build)
- `/specs/api/` - API endpoint specifications
- `/specs/database/` - Schema and model specifications
- `/specs/ui/` - Component and page specifications

## How to Use Specs with Claude Code

1. **Always read relevant spec before implementing**
   ```
   Read @specs/features/task-crud.md before implementing task features
   ```

2. **Reference specs in conversations**
   ```
   @specs/features/authentication.md implement Better Auth login
   ```

3. **Update specs if requirements change**
   - Specs are the source of truth
   - Code should match specs
   - Update specs first, then regenerate code

## Project Structure

```
asif_todo_app_phase2/
├── .spec-kit/              # Spec-Kit configuration
├── specs/                  # All specifications
├── frontend/              # Next.js application
├── backend/               # FastAPI application
├── CLAUDE.md              # This file (root instructions)
└── README.md              # Project documentation
```

## Development Workflow

1. **Read spec**: `@specs/features/[feature].md`
2. **Implement backend**: Follow `@backend/CLAUDE.md`
3. **Implement frontend**: Follow `@frontend/CLAUDE.md`
4. **Test and iterate**: Refine spec if needed

## Commands

### Frontend
```bash
cd frontend
npm install
npm run dev  # http://localhost:3000
```

### Backend
```bash
cd backend
uv sync
uv run uvicorn main:app --reload --port 8000
```

### Full Stack
```bash
# Terminal 1: Backend
cd backend && uv run uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend && npm run dev
```

## Key Principles

1. **Spec-Driven**: Write spec first, then ask Claude Code to implement
2. **No Manual Coding**: Refine specs until Claude Code generates correct output
3. **Better Auth**: Use Better Auth for authentication (not custom localStorage)
4. **RESTful API**: Backend exposes REST API, frontend consumes it
5. **User-Specific Data**: Each user sees only their own tasks

## Phase II Requirements

- ✅ All 5 Basic Level features as web application
- ✅ RESTful API endpoints
- ✅ Responsive frontend interface
- ✅ Neon Serverless PostgreSQL database
- ✅ Better Auth authentication
- ✅ User signup/signin
- ✅ JWT token-based API security

## Referencing Files

- Root instructions: `@CLAUDE.md`
- Frontend guide: `@frontend/CLAUDE.md`
- Backend guide: `@backend/CLAUDE.md`
- Specs: `@specs/[category]/[file].md`

## Hackathon Constraints

⚠️ **IMPORTANT**: You cannot write code manually. You must:
1. Write/refine the specification
2. Ask Claude Code to generate the implementation
3. Test the output
4. If incorrect, refine the spec and regenerate

## Next Steps

1. Review all specs in `/specs` folder
2. Set up Neon PostgreSQL database
3. Implement backend API following `@specs/api/rest-endpoints.md`
4. Implement frontend following `@specs/ui/pages.md`
5. Integrate Better Auth for authentication
6. Test all Basic Level features
7. Deploy to Vercel (frontend) and Railway/Render (backend)

---

**For detailed guidelines, see:**
- Frontend: `@frontend/CLAUDE.md`
- Backend: `@backend/CLAUDE.md`
- Specifications: `@specs/overview.md`
