# Data Model: Phase II Web-Based Todo Application

**Date**: 2026-02-08
**Branch**: 002-web-todo
**Purpose**: Define database schema, entities, relationships, and validation rules

## Entity Relationship Diagram

```
┌─────────────────────────────┐
│          User               │
├─────────────────────────────┤
│ id: int (PK)                │
│ email: str (unique)         │
│ password_hash: str          │
│ created_at: datetime        │
└─────────────────────────────┘
             │
             │ 1:N
             │
             ▼
┌─────────────────────────────┐
│          Task               │
├─────────────────────────────┤
│ id: int (PK)                │
│ user_id: int (FK → User.id) │
│ title: str                  │
│ description: str (nullable) │
│ completed: bool             │
│ created_at: datetime        │
│ updated_at: datetime        │
└─────────────────────────────┘
```

## Entities

### User

**Description**: Represents an authenticated user account with credentials and profile information.

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique user identifier |
| email | String(255) | Unique, Not Null, Indexed | User's email address for authentication |
| password_hash | String(255) | Not Null | Hashed password (managed by Better Auth) |
| created_at | DateTime | Not Null, Default: now() | Account creation timestamp |

**Validation Rules**:
- `email` MUST match email format regex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- `email` MUST be unique across all users
- `password_hash` MUST NOT be exposed in API responses (excluded from serialization)
- `password` (before hashing) MUST be at least 8 characters during registration

**Indexes**:
- Primary index on `id`
- Unique index on `email` for fast lookup during login

**Relationships**:
- One-to-Many with Task: One user can have many tasks

**Business Rules**:
- Email is case-insensitive for uniqueness check (normalized to lowercase before storage)
- Once created, email cannot be changed (no update operation for email in Phase II)
- User deletion (if implemented) must cascade delete all associated tasks

---

### Task

**Description**: Represents a todo item owned by a specific user with title, description, and completion status.

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique task identifier |
| user_id | Integer | Foreign Key → User.id, Not Null, Indexed | Owner of the task |
| title | String(200) | Not Null | Task title/summary |
| description | String(1000) | Nullable | Detailed task description |
| completed | Boolean | Not Null, Default: false | Task completion status |
| created_at | DateTime | Not Null, Default: now() | Task creation timestamp |
| updated_at | DateTime | Not Null, Default: now(), Auto-update | Last modification timestamp |

**Validation Rules**:
- `title` MUST NOT be empty or whitespace-only
- `title` length MUST be between 1 and 200 characters (after trimming whitespace)
- `description` length MUST NOT exceed 1000 characters if provided
- `user_id` MUST reference an existing user (enforced by foreign key constraint)
- `completed` defaults to `false` if not specified

**Indexes**:
- Primary index on `id`
- Foreign key index on `user_id` for fast user-specific queries
- Composite index on `(user_id, created_at)` for sorted task lists

**Relationships**:
- Many-to-One with User: Many tasks belong to one user

**Business Rules**:
- Tasks MUST be owned by exactly one user (user_id cannot be null)
- Tasks can only be accessed, modified, or deleted by their owner
- Toggling `completed` status does NOT change `title` or `description`
- Updating `title` or `description` sets `updated_at` to current timestamp
- Toggling completion also updates `updated_at` timestamp

**State Transitions**:
```
[Task Created] → completed = false
      ↓
[User Toggles] ↔ completed = true
      ↓
[Task Deleted] → removed from database
```

---

## Database Schema (SQL)

```sql
-- Users table
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_user_email ON user(email);

-- Tasks table
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES user(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_user_created ON task(user_id, created_at);

-- Trigger to auto-update updated_at (PostgreSQL)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_task_updated_at
    BEFORE UPDATE ON task
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## SQLModel Definitions (Python)

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class User(SQLModel, table=True):
    """User account with authentication credentials."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user")

    class Config:
        """Exclude password_hash from serialization."""
        fields_to_exclude = {"password_hash"}


class Task(SQLModel, table=True):
    """Todo task item owned by a user."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: User = Relationship(back_populates="tasks")
```

---

## TypeScript Types (Frontend)

```typescript
// src/lib/types.ts

export interface User {
  id: number;
  email: string;
  created_at: string; // ISO 8601 datetime string
}

export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string; // ISO 8601 datetime string
  updated_at: string; // ISO 8601 datetime string
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

export type TaskFilter = 'all' | 'pending' | 'completed';
```

---

## Validation Rules Summary

### User Entity

| Field | Validation Rule | Error Message |
|-------|----------------|---------------|
| email | Required, valid email format, unique | "Invalid email format" / "Email already registered" |
| password | Min 8 characters (before hashing) | "Password must be at least 8 characters" |

### Task Entity

| Field | Validation Rule | Error Message |
|-------|----------------|---------------|
| title | Required, 1-200 chars, not whitespace-only | "Title is required" / "Title too long (max 200 characters)" |
| description | Optional, max 1000 chars | "Description too long (max 1000 characters)" |
| user_id | Must reference existing user | "Invalid user ID" |
| completed | Boolean (true/false) | "Invalid completion status" |

---

## Migration Strategy

### Initial Migration (Alembic)

```bash
# Initialize Alembic
alembic init backend/src/db/migrations

# Edit alembic.ini to set sqlalchemy.url
# Edit env.py to import SQLModel metadata

# Create initial migration
alembic revision --autogenerate -m "Create user and task tables"

# Apply migration
alembic upgrade head
```

### Future Migrations

- Add indexes: `alembic revision -m "Add performance indexes"`
- Add columns: `alembic revision --autogenerate -m "Add user profile fields"`
- Data migrations: Manual SQL in migration file for data transformations

---

## Data Access Patterns

### Common Queries

1. **Get all tasks for a user** (sorted by creation date, newest first):
   ```sql
   SELECT * FROM task
   WHERE user_id = ?
   ORDER BY created_at DESC;
   ```

2. **Get pending tasks for a user**:
   ```sql
   SELECT * FROM task
   WHERE user_id = ? AND completed = false
   ORDER BY created_at DESC;
   ```

3. **Get completed tasks for a user**:
   ```sql
   SELECT * FROM task
   WHERE user_id = ? AND completed = true
   ORDER BY created_at DESC;
   ```

4. **Get single task with ownership check**:
   ```sql
   SELECT * FROM task
   WHERE id = ? AND user_id = ?;
   ```

5. **Find user by email**:
   ```sql
   SELECT * FROM user
   WHERE email = ?;
   ```

### Performance Considerations

- Index on `user_id` enables fast filtering by user (all queries above)
- Composite index on `(user_id, created_at)` optimizes sorted retrieval
- Unique index on `email` enables fast login lookups
- `LIMIT` and `OFFSET` for pagination (future optimization if >1000 tasks)

---

## Security Considerations

1. **Password Storage**: Never store plain-text passwords - Better Auth handles hashing
2. **User ID Validation**: Backend MUST verify JWT user_id matches path user_id before query
3. **SQL Injection Prevention**: Use parameterized queries (SQLModel handles this)
4. **Cascade Deletion**: Deleting a user removes all their tasks (ON DELETE CASCADE)
5. **No Cross-User Access**: All queries include `user_id` filter from authenticated JWT

---

**Data Model Complete**: Ready for contract generation and implementation.
