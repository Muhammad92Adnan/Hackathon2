# Tasks: Phase II Web-Based Todo Application

**Input**: Design documents from `/specs/002-web-todo/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-spec.yaml

**Tests**: Not explicitly requested in specification - omitted for Phase II

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Phase I console app preserved in `src/todo_app/` (not modified)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and monorepo structure

- [X] T001 Create monorepo directory structure (backend/, frontend/) per plan.md
- [X] T002 [P] Initialize backend Python project with requirements.txt (FastAPI, SQLModel, PyJWT, python-jose, Alembic, pytest, httpx)
- [X] T003 [P] Initialize frontend Next.js 16+ project with TypeScript in frontend/ using create-next-app
- [X] T004 [P] Install frontend dependencies: better-auth, tailwindcss, react-hook-form, axios
- [X] T005 [P] Configure Tailwind CSS in frontend/tailwind.config.ts
- [X] T006 [P] Create backend/.env.example with DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS, JWT_ALGORITHM, JWT_EXPIRATION_HOURS
- [X] T007 [P] Create frontend/.env.local.example with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL
- [X] T008 [P] Add .env files to .gitignore (backend/.env, frontend/.env.local)
- [X] T009 [P] Create backend README.md with setup instructions from quickstart.md
- [X] T010 [P] Create frontend README.md with setup instructions from quickstart.md

**Checkpoint**: Project structure ready - foundational work can begin

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [ ] T011 Create database configuration in backend/src/db/database.py (SQLModel engine, session, connection to Neon PostgreSQL)
- [ ] T012 Create config module in backend/src/config.py (load environment variables, validate settings)
- [ ] T013 Initialize Alembic for migrations in backend/src/db/migrations/
- [ ] T014 Create User model in backend/src/models/user.py (SQLModel with id, email, password_hash, created_at)
- [ ] T015 Create Task model in backend/src/models/task.py (SQLModel with id, user_id FK, title, description, completed, created_at, updated_at)
- [ ] T016 Generate initial Alembic migration for User and Task tables
- [ ] T017 Create JWT authentication middleware in backend/src/api/middleware/jwt_auth.py (verify token, extract user_id, validate signature)
- [ ] T018 Create CORS middleware configuration in backend/src/api/main.py
- [ ] T019 Create FastAPI app initialization in backend/src/api/main.py (app instance, middleware, CORS, error handlers)
- [ ] T020 Create base error response schemas in backend/src/api/main.py (HTTPException handlers)

### Frontend Foundation

- [ ] T021 Configure Better Auth in frontend/src/lib/auth.ts (JWT plugin, BETTER_AUTH_SECRET, auth endpoints)
- [ ] T022 Create TypeScript types in frontend/src/lib/types.ts (User, Task, CreateTaskRequest, UpdateTaskRequest, TaskFilter)
- [ ] T023 Create API client in frontend/src/lib/api.ts (axios instance, JWT token injection, error handling)
- [ ] T024 Create authentication hook in frontend/src/hooks/useAuth.ts (login, signup, logout, token management)
- [ ] T025 Create root layout in frontend/src/app/layout.tsx (Better Auth provider, global styles, metadata)
- [ ] T026 Create landing page in frontend/src/app/page.tsx (welcome message, links to signup/login)
- [ ] T027 Create protected route middleware in frontend/src/middleware.ts (redirect to login if not authenticated)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create accounts with email and password

**Independent Test**: Visit registration page, create account, verify user created in database with hashed password

### Implementation for User Story 1

- [ ] T028 [P] [US1] Create UserService in backend/src/services/user_service.py (create_user method with email uniqueness check)
- [ ] T029 [P] [US1] Create auth routes module in backend/src/api/routes/auth.py
- [ ] T030 [US1] Implement POST /api/auth/signup endpoint in backend/src/api/routes/auth.py (validate email/password, create user, return user object)
- [ ] T031 [US1] Add signup route to FastAPI app in backend/src/api/main.py
- [ ] T032 [P] [US1] Create signup page in frontend/src/app/(auth)/signup/page.tsx (form with email/password fields)
- [ ] T033 [P] [US1] Create signup form component in frontend/src/components/SignupForm.tsx (validation, Better Auth integration)
- [ ] T034 [US1] Add error handling for duplicate email in frontend signup form
- [ ] T035 [US1] Add redirect to login page after successful signup

**Checkpoint**: User Story 1 complete - users can register accounts

---

## Phase 4: User Story 2 - User Login & Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable registered users to log in and receive JWT tokens for authentication

**Independent Test**: Log in with valid credentials, verify JWT token issued, access protected routes

### Implementation for User Story 2

- [ ] T036 [US2] Add login method to UserService in backend/src/services/user_service.py (verify email/password, generate JWT token)
- [ ] T037 [US2] Implement POST /api/auth/signin endpoint in backend/src/api/routes/auth.py (authenticate user, return JWT token and user object)
- [ ] T038 [US2] Implement POST /api/auth/signout endpoint in backend/src/api/routes/auth.py (client-side logout message)
- [ ] T039 [P] [US2] Create login page in frontend/src/app/(auth)/login/page.tsx (form with email/password fields)
- [ ] T040 [P] [US2] Create login form component in frontend/src/components/LoginForm.tsx (validation, Better Auth integration, token storage)
- [ ] T041 [US2] Add error handling for invalid credentials in frontend login form
- [ ] T042 [US2] Add redirect to dashboard after successful login
- [ ] T043 [US2] Implement token persistence across page refreshes using localStorage
- [ ] T044 [US2] Add JWT token expiration handling (redirect to login on 401 errors)

**Checkpoint**: User Story 2 complete - users can log in and access authenticated routes

---

## Phase 5: User Story 3 - Add Tasks via Web UI (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to create new tasks with title and description

**Independent Test**: Log in, add task with title/description, verify task appears in list and is saved to database

### Implementation for User Story 3

- [ ] T045 [US3] Create TaskService in backend/src/services/task_service.py (create_task, get_tasks_for_user methods)
- [ ] T046 [US3] Create task routes module in backend/src/api/routes/tasks.py
- [ ] T047 [US3] Implement POST /api/{user_id}/tasks endpoint in backend/src/api/routes/tasks.py (validate user_id matches JWT, create task)
- [ ] T048 [US3] Add JWT middleware to task routes to extract and validate user_id
- [ ] T049 [US3] Add user_id path parameter validation (403 if path user_id != JWT user_id)
- [ ] T050 [US3] Add task routes to FastAPI app in backend/src/api/main.py
- [ ] T051 [P] [US3] Create useTasks hook in frontend/src/hooks/useTasks.ts (fetch, create, update, delete, toggle methods)
- [ ] T052 [P] [US3] Create TaskForm component in frontend/src/components/TaskForm.tsx (title/description inputs, validation)
- [ ] T053 [US3] Add task creation API call in TaskForm using useTasks hook
- [ ] T054 [US3] Add validation error handling (title required, max lengths)
- [ ] T055 [US3] Add success message after task creation

**Checkpoint**: User Story 3 complete - users can create tasks

---

## Phase 6: User Story 4 - View Personal Task List (Priority: P1) 🎯 MVP

**Goal**: Enable users to view all their tasks with completion status

**Independent Test**: Create multiple tasks, verify all appear with correct details and status, verify only user's own tasks shown

### Implementation for User Story 4

- [ ] T056 [US4] Implement GET /api/{user_id}/tasks endpoint in backend/src/api/routes/tasks.py (filter by user_id, support ?status query param)
- [ ] T057 [US4] Add user_id validation to GET endpoint (403 if mismatch)
- [ ] T058 [US4] Create dashboard page in frontend/src/app/dashboard/page.tsx (protected route, fetch and display tasks)
- [ ] T059 [P] [US4] Create TaskList component in frontend/src/components/TaskList.tsx (render array of tasks)
- [ ] T060 [P] [US4] Create TaskItem component in frontend/src/components/TaskItem.tsx (display title, description, completed status)
- [ ] T061 [US4] Add empty state message in TaskList when no tasks exist
- [ ] T062 [US4] Add loading state while fetching tasks
- [ ] T063 [US4] Add error handling for failed task fetch
- [ ] T064 [P] [US4] Create Header component in frontend/src/components/Header.tsx (navigation, user email, logout button)
- [ ] T065 [US4] Integrate Header into dashboard layout

**Checkpoint**: User Story 4 complete - users can view their task list

---

## Phase 7: User Story 5 - Mark Tasks Complete (Priority: P2)

**Goal**: Enable users to toggle task completion status

**Independent Test**: Mark task as complete, verify status persists in database, toggle back to incomplete

### Implementation for User Story 5

- [ ] T066 [US5] Add toggle_task method to TaskService in backend/src/services/task_service.py
- [ ] T067 [US5] Implement PATCH /api/{user_id}/tasks/{task_id}/toggle endpoint in backend/src/api/routes/tasks.py
- [ ] T068 [US5] Add ownership validation (verify task belongs to user_id from JWT)
- [ ] T069 [US5] Add checkbox to TaskItem component for toggling completion status
- [ ] T070 [US5] Add toggle API call in useTasks hook
- [ ] T071 [US5] Update TaskItem to call toggle on checkbox click
- [ ] T072 [US5] Add optimistic UI update (update immediately, rollback on error)

**Checkpoint**: User Story 5 complete - users can toggle task completion

---

## Phase 8: User Story 6 - Update Tasks (Priority: P2)

**Goal**: Enable users to edit task title and description

**Independent Test**: Edit task details, verify changes persist in database and display immediately

### Implementation for User Story 6

- [ ] T073 [US6] Add update_task method to TaskService in backend/src/services/task_service.py
- [ ] T074 [US6] Implement PUT /api/{user_id}/tasks/{task_id} endpoint in backend/src/api/routes/tasks.py
- [ ] T075 [US6] Add ownership validation to PUT endpoint
- [ ] T076 [US6] Add edit mode state to TaskItem component (toggle between view/edit)
- [ ] T077 [US6] Add inline editing fields in TaskItem (title/description inputs)
- [ ] T078 [US6] Add update API call in useTasks hook
- [ ] T079 [US6] Add save/cancel buttons in edit mode
- [ ] T080 [US6] Add validation for edited fields (title required, max lengths)

**Checkpoint**: User Story 6 complete - users can edit tasks

---

## Phase 9: User Story 7 - Delete Tasks (Priority: P3)

**Goal**: Enable users to delete tasks permanently

**Independent Test**: Delete task, verify removed from UI and database

### Implementation for User Story 7

- [ ] T081 [US7] Add delete_task method to TaskService in backend/src/services/task_service.py
- [ ] T082 [US7] Implement DELETE /api/{user_id}/tasks/{task_id} endpoint in backend/src/api/routes/tasks.py
- [ ] T083 [US7] Add ownership validation to DELETE endpoint
- [ ] T084 [US7] Add delete button to TaskItem component
- [ ] T085 [US7] Add confirmation dialog before deletion
- [ ] T086 [US7] Add delete API call in useTasks hook
- [ ] T087 [US7] Remove task from UI immediately after successful deletion

**Checkpoint**: User Story 7 complete - users can delete tasks

---

## Phase 10: User Story 8 - User Logout (Priority: P2)

**Goal**: Enable users to log out and clear authentication session

**Independent Test**: Log out, verify session cleared, protected routes inaccessible

### Implementation for User Story 8

- [ ] T088 [US8] Add logout functionality to useAuth hook (clear JWT token from localStorage)
- [ ] T089 [US8] Add logout button to Header component
- [ ] T090 [US8] Call logout on button click and redirect to login page
- [ ] T091 [US8] Add protected route check on dashboard (redirect if no token)

**Checkpoint**: User Story 8 complete - users can log out securely

---

## Phase 11: User Story 9 - Filter Tasks by Status (Priority: P2)

**Goal**: Enable users to filter tasks by all/pending/completed status

**Independent Test**: Create tasks with different statuses, verify each filter shows correct subset

### Implementation for User Story 9

- [ ] T092 [P] [US9] Create TaskFilter component in frontend/src/components/TaskFilter.tsx (buttons for All/Pending/Completed)
- [ ] T093 [US9] Add filter state to dashboard page (all, pending, completed)
- [ ] T094 [US9] Implement client-side filtering logic in TaskList component
- [ ] T095 [US9] Integrate TaskFilter into dashboard page
- [ ] T096 [US9] Highlight active filter button
- [ ] T097 [US9] Update task count display to show filtered count

**Checkpoint**: User Story 9 complete - users can filter tasks by status

---

## Phase 12: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and deployment preparation

### Environment & Configuration

- [ ] T098 [P] Create backend/.env file with actual Neon PostgreSQL connection string
- [ ] T099 [P] Create frontend/.env.local with actual backend API URL
- [ ] T100 [P] Generate BETTER_AUTH_SECRET and add to both backend/.env and frontend/.env.local (must be identical)
- [ ] T101 Apply Alembic migrations to Neon database (alembic upgrade head)

### Code Quality & Documentation

- [ ] T102 [P] Add docstrings to all backend models, services, and routes
- [ ] T103 [P] Add TypeScript JSDoc comments to all frontend components and hooks
- [ ] T104 [P] Add error logging to backend API endpoints
- [ ] T105 [P] Add console error logging to frontend API client
- [ ] T106 [P] Update root README.md with Phase II overview and links to backend/frontend READMEs

### Deployment Preparation

- [ ] T107 Configure Vercel deployment for frontend (vercel.json if needed)
- [ ] T108 Configure Railway/Render deployment for backend (Procfile or start command)
- [ ] T109 Set environment variables in Vercel dashboard for frontend
- [ ] T110 Set environment variables in Railway/Render dashboard for backend
- [ ] T111 Update CORS_ORIGINS in backend to include production frontend URL
- [ ] T112 Deploy frontend to Vercel
- [ ] T113 Deploy backend to Railway/Render
- [ ] T114 Verify database connection from deployed backend

### Validation & Demo

- [ ] T115 Run quickstart.md validation (test all user flows locally)
- [ ] T116 Test complete user journey on deployed application (signup → login → CRUD → filter → logout)
- [ ] T117 Record demo video (under 90 seconds) showing core features
- [ ] T118 Create deployment documentation with URLs and setup notes

**Checkpoint**: Phase II complete and deployed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-11)**: All depend on Foundational phase completion
  - US1 (Registration) → US2 (Login) → US3 (Add Tasks) → US4 (View Tasks) have logical dependencies
  - US5 (Toggle), US6 (Update), US7 (Delete), US8 (Logout), US9 (Filter) can proceed in parallel after US4
- **Polish (Phase 12)**: Depends on all user stories being complete

### User Story Dependencies

**MVP Core (Must complete in order)**:
- **User Story 1 (Registration)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (Login)**: Depends on US1 (users must exist to log in)
- **User Story 3 (Add Tasks)**: Depends on US2 (must be logged in to create tasks)
- **User Story 4 (View Tasks)**: Depends on US3 (tasks must exist to view)

**Secondary Features (Can parallelize after US4)**:
- **User Story 5 (Toggle Complete)**: Depends on US4 (needs tasks to toggle)
- **User Story 6 (Update Tasks)**: Depends on US4 (needs tasks to update)
- **User Story 7 (Delete Tasks)**: Depends on US4 (needs tasks to delete)
- **User Story 8 (Logout)**: Depends on US2 (needs login to log out)
- **User Story 9 (Filter Tasks)**: Depends on US4 (needs tasks to filter)

### Within Each User Story

- Backend services before endpoints
- Backend endpoints before frontend hooks
- Frontend hooks before components
- Core components before UI polish
- Validation before error handling

### Parallel Opportunities

**Setup Phase (Phase 1)**:
- T002 (backend init) || T003 (frontend init) || T004 (frontend deps)
- T005 (tailwind) || T006 (backend .env) || T007 (frontend .env) || T008 (gitignore) || T009 (backend README) || T010 (frontend README)

**Foundational Phase (Phase 2)**:
- Backend foundation (T011-T020) can proceed in parallel with Frontend foundation (T021-T027)

**User Story Tasks**:
- Backend and frontend tasks within same story can often parallelize (different files)
- Example US1: T028 (UserService) || T029 (auth routes) can run in parallel with T032 (signup page) || T033 (signup form)

**Polish Phase (Phase 12)**:
- T098 (backend .env) || T099 (frontend .env) || T100 (secret) || T102 (docstrings) || T103 (JSDoc) || T104 (backend logging) || T105 (frontend logging) || T106 (README)

---

## Parallel Example: User Story 1 (Registration)

```bash
# Backend tasks (can run in parallel):
Task T028: "Create UserService in backend/src/services/user_service.py"
Task T029: "Create auth routes module in backend/src/api/routes/auth.py"

# Then (depends on T028, T029):
Task T030: "Implement POST /api/auth/signup endpoint"
Task T031: "Add signup route to FastAPI app"

# Frontend tasks (can run in parallel with backend tasks):
Task T032: "Create signup page in frontend/src/app/(auth)/signup/page.tsx"
Task T033: "Create signup form component in frontend/src/components/SignupForm.tsx"

# Then (depends on T032, T033):
Task T034: "Add error handling for duplicate email"
Task T035: "Add redirect to login page after successful signup"
```

---

## Implementation Strategy

### MVP First (User Stories 1-4 Only)

1. Complete Phase 1: Setup → Project structure ready
2. Complete Phase 2: Foundational → Database, auth middleware, Better Auth configured
3. Complete Phase 3: User Story 1 (Registration) → Users can sign up
4. Complete Phase 4: User Story 2 (Login) → Users can authenticate
5. Complete Phase 5: User Story 3 (Add Tasks) → Users can create tasks
6. Complete Phase 6: User Story 4 (View Tasks) → Users can see their tasks
7. **STOP and VALIDATE**: Test complete user journey (signup → login → add task → view tasks)
8. Deploy MVP and create demo video

**MVP Scope**: 66 tasks (T001-T065, plus T098-T101 for deployment)

### Incremental Delivery

1. **Foundation** (Phase 1-2): Setup + Foundational → Deploy empty app with auth
2. **MVP** (Phase 3-6): Add US1-US4 → Deploy functional todo app
3. **Enhancement 1** (Phase 7-8): Add US5 (Toggle) + US8 (Logout) → Deploy with completion tracking
4. **Enhancement 2** (Phase 9, 11): Add US6 (Update) + US9 (Filter) → Deploy with editing and filtering
5. **Final** (Phase 10, 12): Add US7 (Delete) + Polish → Deploy complete application

### Parallel Team Strategy

With 3 developers after Foundational phase completes:

1. **Developer A**: User Stories 1-2 (Auth flow)
2. **Developer B**: User Stories 3-4 (Task CRUD foundation)
3. **Developer C**: Setup deployment infrastructure (T107-T111)

Then after US1-4 complete:
1. **Developer A**: User Stories 5, 8 (Toggle, Logout)
2. **Developer B**: User Stories 6, 7 (Update, Delete)
3. **Developer C**: User Story 9 (Filter) + Polish tasks

---

## Task Summary

**Total Tasks**: 118
- **Phase 1 (Setup)**: 10 tasks
- **Phase 2 (Foundational)**: 17 tasks (Backend: 10, Frontend: 7)
- **Phase 3 (US1 - Registration)**: 8 tasks
- **Phase 4 (US2 - Login)**: 9 tasks
- **Phase 5 (US3 - Add Tasks)**: 11 tasks
- **Phase 6 (US4 - View Tasks)**: 10 tasks
- **Phase 7 (US5 - Toggle)**: 7 tasks
- **Phase 8 (US6 - Update)**: 8 tasks
- **Phase 9 (US7 - Delete)**: 7 tasks
- **Phase 10 (US8 - Logout)**: 4 tasks
- **Phase 11 (US9 - Filter)**: 6 tasks
- **Phase 12 (Polish)**: 21 tasks

**Tasks by User Story**:
- US1 (Registration): 8 tasks (T028-T035)
- US2 (Login): 9 tasks (T036-T044)
- US3 (Add Tasks): 11 tasks (T045-T055)
- US4 (View Tasks): 10 tasks (T056-T065)
- US5 (Toggle Complete): 7 tasks (T066-T072)
- US6 (Update Tasks): 8 tasks (T073-T080)
- US7 (Delete Tasks): 7 tasks (T081-T087)
- US8 (Logout): 4 tasks (T088-T091)
- US9 (Filter Tasks): 6 tasks (T092-T097)

**Parallel Opportunities**: 45 tasks marked with [P] for parallel execution

**MVP Scope**: User Stories 1-4 = 38 implementation tasks + 27 foundational tasks = 65 core tasks

**Independent Test Criteria**: Each user story phase includes checkpoint with clear acceptance criteria

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label (US1-US9) maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All file paths are explicit and ready for implementation
- Backend uses FastAPI + SQLModel, Frontend uses Next.js 16+ + TypeScript + Better Auth
- Phase I console app in src/todo_app/ is preserved and not modified
