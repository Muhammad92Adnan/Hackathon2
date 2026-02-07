---

description: "Task list for Phase I Console Todo Application implementation"
---

# Tasks: Phase I Console Todo Application

**Input**: Design documents from `/specs/001-console-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Tests are included as this is a core application feature requiring validation of all CRUD operations.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow the plan.md structure for console application

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan with src/todo_app/ and tests/ directories
- [X] T002 Initialize Python project with pyproject.toml for uv package manager
- [X] T003 [P] Configure pytest in pyproject.toml with test discovery settings
- [X] T004 [P] Create src/todo_app/__init__.py with package initialization
- [X] T005 [P] Create empty __init__.py files in src/todo_app/models/, src/todo_app/services/, src/todo_app/cli/, src/todo_app/utils/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Create Task model in src/todo_app/models/task.py with id, title, description, completed attributes
- [X] T007 [P] Implement input validators in src/todo_app/utils/validators.py for title and ID validation
- [X] T008 Create TodoService skeleton in src/todo_app/services/todo_service.py with in-memory storage initialization
- [X] T009 [P] Create CLI main menu structure in src/todo_app/cli/main_menu.py with menu loop
- [X] T010 Create application entry point in src/todo_app/__main__.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new todo items with title and description

**Independent Test**: Can be fully tested by launching the CLI and successfully adding new tasks with titles and descriptions that persist in memory during the session.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T011 [P] [US1] Create unit test for Task model creation in tests/unit/test_task.py
- [X] T012 [P] [US1] Create unit test for add_task method in tests/unit/test_todo_service.py
- [X] T013 [US1] Create integration test for add task CLI flow in tests/integration/test_cli_integration.py

### Implementation for User Story 1

- [X] T014 [US1] Implement Task model __init__ method with validation in src/todo_app/models/task.py
- [X] T015 [US1] Implement add_task method in TodoService in src/todo_app/services/todo_service.py
- [X] T016 [US1] Implement "Add Task" menu option in main_menu.py with user input prompts
- [X] T017 [US1] Add title validation with error handling for empty titles
- [X] T018 [US1] Verify Task ID auto-increment functionality works correctly

**Checkpoint**: At this point, User Story 1 should be fully functional - users can add tasks and they appear in memory

---

## Phase 4: User Story 2 - View Task List (Priority: P1)

**Goal**: Enable users to view all tasks with status indicators

**Independent Test**: Can be fully tested by adding tasks and then viewing the task list to confirm all tasks appear with proper status indicators.

### Tests for User Story 2

- [X] T019 [P] [US2] Create unit test for list_tasks method in tests/unit/test_todo_service.py
- [X] T020 [US2] Create integration test for view task list CLI flow in tests/integration/test_cli_integration.py

### Implementation for User Story 2

- [X] T021 [US2] Implement list_tasks method in TodoService in src/todo_app/services/todo_service.py
- [X] T022 [US2] Implement task display formatting with ID, title, description, and completion status
- [X] T023 [US2] Implement "View Task List" menu option in main_menu.py
- [X] T024 [US2] Add empty list handling with appropriate message display

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - users can add and view tasks

---

## Phase 5: User Story 3 - Mark Tasks as Complete (Priority: P2)

**Goal**: Enable users to toggle the completion status of tasks

**Independent Test**: Can be fully tested by marking tasks as complete/incomplete and verifying the status updates in the task list.

### Tests for User Story 3

- [X] T025 [P] [US3] Create unit test for toggle_complete method in tests/unit/test_todo_service.py
- [X] T026 [US3] Create integration test for mark complete CLI flow in tests/integration/test_cli_integration.py

### Implementation for User Story 3

- [X] T027 [US3] Implement toggle_complete method in TodoService in src/todo_app/services/todo_service.py
- [X] T028 [US3] Implement "Mark as Complete" menu option in main_menu.py with task ID input
- [X] T029 [US3] Add validation for invalid task IDs with error messages
- [X] T030 [US3] Update task display to show completion status clearly (e.g., [X] or [ ])

**Checkpoint**: Users can now add, view, and mark tasks as complete

---

## Phase 6: User Story 4 - Update Existing Tasks (Priority: P2)

**Goal**: Enable users to modify existing task details (title, description)

**Independent Test**: Can be fully tested by updating task details and verifying the changes are reflected in the system.

### Tests for User Story 4

- [X] T031 [P] [US4] Create unit test for update_task method in tests/unit/test_todo_service.py
- [X] T032 [US4] Create integration test for update task CLI flow in tests/integration/test_cli_integration.py

### Implementation for User Story 4

- [X] T033 [US4] Implement update_task method in TodoService in src/todo_app/services/todo_service.py
- [X] T034 [US4] Implement "Update Task" menu option in main_menu.py with task selection
- [X] T035 [US4] Add prompts for updating title and/or description
- [X] T036 [US4] Add validation for invalid task IDs and empty titles

**Checkpoint**: Users can now add, view, mark complete, and update tasks

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P3)

**Goal**: Enable users to remove tasks from their list by ID

**Independent Test**: Can be fully tested by deleting a task and confirming it no longer appears in the task list.

### Tests for User Story 5

- [X] T037 [P] [US5] Create unit test for delete_task method in tests/unit/test_todo_service.py
- [X] T038 [US5] Create integration test for delete task CLI flow in tests/integration/test_cli_integration.py

### Implementation for User Story 5

- [X] T039 [US5] Implement delete_task method in TodoService in src/todo_app/services/todo_service.py
- [X] T040 [US5] Implement "Delete Task" menu option in main_menu.py with task ID input
- [X] T041 [US5] Add confirmation prompt before deleting task
- [X] T042 [US5] Add validation for invalid task IDs with error messages

**Checkpoint**: All 5 core CRUD operations are now fully functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and project deliverables

- [X] T043 [P] Create README.md with setup instructions for uv install and run commands
- [X] T044 [P] Create CLAUDE.md with Claude Code instructions for the project
- [X] T045 Add docstrings to all classes and methods following PEP 8 standards
- [X] T046 Add type hints to all function parameters and return values
- [X] T047 [P] Create tests/conftest.py with pytest fixtures for common test setup
- [X] T048 Add exit option to main menu for clean application shutdown
- [X] T049 Add error handling for unexpected exceptions with user-friendly messages
- [X] T050 Run all tests to validate complete application functionality

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P1 → P2 → P2 → P3)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Integrates with US1 for viewing added tasks
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Uses tasks from US1, displays in US2
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Updates tasks from US1
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Deletes tasks from US1

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before CLI implementation
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004, T005)
- Foundational validation (T007) can run parallel with model creation (T006)
- All tests for a user story marked [P] can run in parallel
- Documentation tasks (T043, T044) can run in parallel
- Different user stories can be worked on in parallel by different team members after Phase 2

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Create unit test for Task model creation in tests/unit/test_task.py"
Task: "Create unit test for add_task method in tests/unit/test_todo_service.py"

# These can run in parallel since they're different files
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add Tasks)
4. Complete Phase 4: User Story 2 (View Tasks)
5. **STOP and VALIDATE**: Test that adding and viewing tasks works independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 + User Story 2 → Test independently → Deploy/Demo (MVP - basic todo list!)
3. Add User Story 3 → Test independently → Deploy/Demo (Can now complete tasks)
4. Add User Story 4 → Test independently → Deploy/Demo (Can now edit tasks)
5. Add User Story 5 → Test independently → Deploy/Demo (Full CRUD functionality)
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 + User Story 2 (core MVP)
   - Developer B: User Story 3 + User Story 4 (enhancement features)
   - Developer C: User Story 5 + Documentation (cleanup features)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Follow PEP 8, use docstrings and type hints as per constitution requirements
- In-memory storage only - no file or database persistence
