---
id: 0002
title: Phase II Web Todo Spec Update
stage: spec
date: 2026-02-08
surface: agent
model: Claude Sonnet 4.5
feature: 002-web-todo
branch: 002-web-todo
user: user
command: /sp.specify
labels: ["spec", "phase-ii", "web-app", "better-auth", "jwt", "task-filtering", "api-endpoints"]
links:
  spec: ../specs/002-web-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-web-todo/spec.md
  - specs/002-web-todo/checklists/requirements.md
tests: []
---

## Prompt

User provided refined Phase II specification with specific requirements:

Phase II: Full-Stack Web Todo App with Authentication

Transform console app into modern multi-user web application with persistent storage.

Core Features:
1. User Authentication - Better Auth with JWT plugin
2. Web Interface - Next.js 16+ (App Router) with React 19+ and TypeScript
3. PostgreSQL Database - Neon Serverless PostgreSQL
4. REST API - FastAPI backend with SQLModel ORM
5. Task Filtering - View tasks by status (all, pending, completed)
6. All Phase I CRUD Operations - Add, View, Update, Delete, Mark Complete

API Endpoints (JWT required):
- GET /api/{user_id}/tasks - List all tasks (supports ?status filter)
- POST /api/{user_id}/tasks - Create new task
- GET /api/{user_id}/tasks/{task_id} - Get task details
- PUT /api/{user_id}/tasks/{task_id} - Update task
- PATCH /api/{user_id}/tasks/{task_id}/toggle - Toggle completion
- DELETE /api/{user_id}/tasks/{task_id} - Delete task

Authentication (Better Auth + JWT):
- User signup/signin via Better Auth (frontend)
- Better Auth issues JWT tokens using JWT plugin
- Frontend includes JWT in Authorization header
- Backend validates JWT using shared BETTER_AUTH_SECRET
- Backend verifies user_id in URL matches JWT user_id claim

Technology Stack:
Frontend: Next.js 16+, React 19+, TypeScript, Tailwind CSS, Better Auth
Backend: FastAPI (Python 3.13+), SQLModel, Pydantic, JWT validation, CORS
Database: Neon Serverless PostgreSQL with SQLModel migrations

Deliverables:
- Frontend deployed to Vercel
- Backend deployed to Railway/Render
- Neon PostgreSQL configured
- Environment variables documented (.env)
- Demo video (under 90 seconds) showing signup, login, CRUD, filtering, logout
- Monorepo structure (frontend/ and backend/ directories)

## Response snapshot

Updated Phase II specification with refined requirements:

**Key Changes from Initial Spec:**
1. Added User Story 9 - Task filtering by status (all, pending, completed)
2. Expanded functional requirements from 22 to 32 requirements:
   - Better Auth with JWT plugin specified (FR-001 to FR-008 for auth)
   - Explicit user_id validation in API endpoints (FR-021)
   - Task filtering support (FR-013, FR-024)
   - Better Auth and deployment-specific requirements (FR-025 to FR-032)
3. Added explicit API Endpoint Structure section documenting all 9 endpoints
4. Expanded success criteria from 10 to 13 criteria (added filtering, deployment, demo video)
5. Updated assumptions to include Better Auth, BETTER_AUTH_SECRET, monorepo structure, demo video
6. Added comprehensive edge cases for JWT validation, user_id mismatch, and task filtering

**Technology Stack Validation:**
- User confirmed to keep tech stack in spec despite "no implementation details" principle
- Rationale: Hackathon constitution pre-defines technology stack for each phase
- Checklist updated with exception noted for hackathon context

**Validation Status:**
✅ All 12 checklist items pass (with hackathon exception for tech stack)
✅ No [NEEDS CLARIFICATION] markers
✅ 9 user stories with clear priorities
✅ 32 testable functional requirements
✅ 13 measurable success criteria
✅ Comprehensive edge cases and assumptions

## Outcome

- ✅ Impact: Phase II specification refined and ready for planning phase
- 🧪 Tests: No test implementation (specification phase)
- 📁 Files: spec.md and requirements checklist updated
- 🔁 Next prompts: Ready for /sp.plan to create implementation plan
- 🧠 Reflection: Specification successfully updated with Better Auth JWT details, API structure, and task filtering. User decision to keep tech stack aligns spec with hackathon constitution.

## Evaluation notes (flywheel)

- Failure modes observed: Initial validation flagged tech stack as implementation details, resolved by user confirming hackathon exception
- Graders run and results (PASS/FAIL): Checklist validation PASS (12/12 items with noted exception)
- Prompt variant (if applicable): Refined specification workflow with user clarification on tech stack handling
- Next experiment (smallest change to try): Proceed to /sp.plan phase with Better Auth JWT plugin and API endpoint architecture
