# Implementation Plan: Phase II Web-Based Todo Application

**Branch**: `002-web-todo` | **Date**: 2026-02-08 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-web-todo/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Transform the Phase I console todo application into a full-stack web application with multi-user authentication, persistent PostgreSQL storage, and modern web UI. Users will be able to register, log in, and manage their personal todo lists through a responsive web interface built with Next.js and React. The backend FastAPI service will expose RESTful endpoints secured with JWT tokens, ensuring users can only access their own tasks. All data will persist in Neon PostgreSQL with proper user-task relationships.

## Technical Context

**Frontend**:
- **Language/Version**: TypeScript with Next.js 16+ (App Router), React 19+
- **Primary Dependencies**: Better Auth (with JWT plugin), Tailwind CSS, React Hook Form, Axios/Fetch API
- **Testing**: Vitest or Jest for unit tests, React Testing Library, Playwright for E2E
- **Target Platform**: Modern browsers (Chrome, Firefox, Safari, Edge) with responsive design (320px minimum width)
- **Deployment**: Vercel with automatic HTTPS

**Backend**:
- **Language/Version**: Python 3.13+
- **Primary Dependencies**: FastAPI, SQLModel (ORM), Pydantic (validation), PyJWT (JWT validation), python-jose, CORS middleware
- **Storage**: Neon Serverless PostgreSQL with SQLModel migrations
- **Testing**: pytest with async support, httpx for API testing
- **Target Platform**: Linux server (Railway/Render deployment)
- **Deployment**: Railway or Render with automatic HTTPS

**Project Type**: Web application (monorepo with frontend/ and backend/ directories)

**Performance Goals**:
- API response time: <2 seconds for task operations
- Page load: <3 seconds on typical broadband
- Database queries: <100ms for up to 1000 tasks per user
- Password hashing: <500ms during registration/login

**Constraints**:
- JWT tokens valid for 24 hours
- Task title max 200 characters, description max 1000 characters
- Mobile responsive (minimum 320px width)
- HTTPS required in production
- Shared BETTER_AUTH_SECRET between frontend and backend for JWT verification

**Scale/Scope**:
- Multi-user application (hundreds to thousands of users expected)
- Each user can have unlimited tasks (optimized for <1000 tasks per user)
- 9 API endpoints (3 auth + 6 task management)
- 6-8 React pages/components (Login, Signup, Dashboard, Task List, Task Form, Task Filters)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **Spec-Driven Development**: All code will be generated via `/sp.implement` from specs/plan/tasks - no manual coding

✅ **Phase-Based Evolution**: This is Phase II (Web) following completed Phase I (Console) - correct sequence

✅ **Technology Stack Compliance**:
- Frontend: Next.js 16+, React 19+, TypeScript, Tailwind CSS, Better Auth ✅ (matches constitution Phase II requirements)
- Backend: FastAPI, SQLModel, Neon PostgreSQL ✅ (matches constitution Phase II requirements)
- Authentication: Better Auth with JWT plugin ✅ (matches constitution security requirements)

✅ **Monorepo Organization**: frontend/ and backend/ directory structure planned

✅ **Security & Secrets**: BETTER_AUTH_SECRET, database credentials, and API keys in environment variables (.env files)

✅ **Clean Code Standards**: Will include docstrings, type hints, descriptive naming

✅ **Traceability**: All code changes will map back to spec.md → plan.md → tasks.md

**Gate Status**: ✅ PASS - Proceed to Phase 0 research

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── user.py          # User model with SQLModel
│   │   └── task.py          # Task model with SQLModel
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py      # Better Auth integration endpoints
│   │   │   └── tasks.py     # Task CRUD endpoints
│   │   ├── middleware/
│   │   │   └── jwt_auth.py  # JWT validation middleware
│   │   └── main.py          # FastAPI app initialization
│   ├── services/
│   │   ├── user_service.py  # User business logic
│   │   └── task_service.py  # Task business logic
│   ├── db/
│   │   ├── database.py      # SQLModel engine and session
│   │   └── migrations/      # Database migrations (Alembic)
│   └── config.py            # Environment configuration
├── tests/
│   ├── unit/
│   │   ├── test_models.py
│   │   └── test_services.py
│   ├── integration/
│   │   └── test_api.py
│   └── conftest.py          # Pytest fixtures
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md

frontend/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── signup/
│   │   │       └── page.tsx
│   │   ├── dashboard/
│   │   │   └── page.tsx     # Main task dashboard
│   │   ├── layout.tsx       # Root layout with Better Auth
│   │   └── page.tsx         # Landing page
│   ├── components/
│   │   ├── TaskList.tsx     # Task list with filtering
│   │   ├── TaskForm.tsx     # Add/Edit task form
│   │   ├── TaskItem.tsx     # Individual task card
│   │   ├── TaskFilter.tsx   # Filter buttons (all/pending/completed)
│   │   └── Header.tsx       # Navigation with logout
│   ├── lib/
│   │   ├── auth.ts          # Better Auth configuration
│   │   ├── api.ts           # API client with JWT handling
│   │   └── types.ts         # TypeScript types
│   └── hooks/
│       ├── useAuth.ts       # Authentication hook
│       └── useTasks.ts      # Task management hook
├── tests/
│   ├── components/
│   └── e2e/
├── public/
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── .env.example
└── README.md

# Phase I code remains in src/ and tests/ (console app)
src/
└── todo_app/               # Phase I console app (preserved)
```

**Structure Decision**: Web application monorepo structure selected. Frontend uses Next.js 16+ App Router with TypeScript and React 19+. Backend uses FastAPI with SQLModel for database operations. Phase I console application code remains in src/ directory and is not modified in Phase II.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations detected. All architectural decisions align with Phase II requirements.

---

## Phase 0 & Phase 1 Completion Summary

### Phase 0: Research ✅

**Artifact**: `research.md`

**Completed Research**:
1. ✅ Better Auth JWT Plugin integration strategy
2. ✅ API endpoint design with user_id in path
3. ✅ Task filtering implementation approach (client-side Phase II)
4. ✅ Database schema and migration strategy (SQLModel + Alembic)
5. ✅ CORS configuration for frontend-backend communication
6. ✅ Environment variables and secret management
7. ✅ Testing strategy (pytest, Vitest, Playwright)
8. ✅ Deployment strategy (Vercel, Railway, Neon)

**Key Decisions**:
- Use Better Auth JWT plugin for token generation
- Validate JWT on backend with shared BETTER_AUTH_SECRET
- Include user_id in URL path for explicit authorization
- Client-side task filtering for Phase II (API supports server-side for future)
- SQLModel for type-safe ORM with Alembic migrations
- Neon Serverless PostgreSQL for database

### Phase 1: Design & Contracts ✅

**Artifacts**:
- `data-model.md` - Database schema with User and Task entities
- `contracts/api-spec.yaml` - OpenAPI 3.0 specification for all 9 endpoints
- `quickstart.md` - Local setup and deployment guide

**Data Model**:
- User entity: id, email (unique), password_hash, created_at
- Task entity: id, user_id (FK), title, description, completed, created_at, updated_at
- Relationship: User 1:N Task
- Indexes: email (unique), user_id, (user_id, created_at)

**API Contracts**:
- 3 Authentication endpoints: /api/auth/signup, /api/auth/signin, /api/auth/signout
- 6 Task endpoints: GET/POST /api/{user_id}/tasks, GET/PUT/DELETE/PATCH /api/{user_id}/tasks/{task_id}
- All task endpoints require JWT authorization
- All task endpoints validate path user_id matches JWT user_id

**Project Structure**:
- Monorepo: frontend/ and backend/ directories
- Frontend: Next.js 16+ App Router with TypeScript and Tailwind CSS
- Backend: FastAPI with SQLModel, Pydantic validation, JWT middleware
- Phase I console app preserved in src/ (not modified)

**Agent Context Updated**:
- CLAUDE.md updated with Phase II technology stack
- Added Better Auth, Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL context

### Re-evaluated Constitution Check ✅

All gates still pass after design phase:

✅ **Spec-Driven Development**: Plan follows spec-driven workflow
✅ **Phase-Based Evolution**: Correct sequence (Phase I complete → Phase II design)
✅ **Technology Stack**: All choices match constitution Phase II requirements
✅ **Monorepo Organization**: frontend/ and backend/ structure defined
✅ **Security & Secrets**: All secrets in environment variables
✅ **Clean Code Standards**: Docstrings, type hints, descriptive naming planned
✅ **Traceability**: All artifacts link back to spec.md

**Gate Status**: ✅ PASS - Ready for `/sp.tasks` to generate task breakdown

---

## Next Phase

**Command**: `/sp.tasks`

**Purpose**: Generate tasks.md with detailed implementation tasks based on:
- Feature spec (spec.md)
- Implementation plan (this file)
- Research decisions (research.md)
- Data model (data-model.md)
- API contracts (contracts/api-spec.yaml)

**Expected Output**:
- Dependency-ordered tasks for frontend and backend implementation
- Test-first tasks (write tests before implementation)
- Tasks organized by user story for traceability
- Parallel execution opportunities marked

