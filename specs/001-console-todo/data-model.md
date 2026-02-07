# Data Model: Phase I Console Todo Application

## Task Entity

### Attributes
- **id**: Integer (Auto-generated, unique identifier)
  - Purpose: Unique identifier for each task
  - Constraints: Auto-incrementing integer, unique within the application session

- **title**: String (Required, min 1 character)
  - Purpose: Brief description or name of the task
  - Constraints: Cannot be empty or whitespace-only, max 200 characters

- **description**: String (Optional)
  - Purpose: Detailed information about the task
  - Constraints: Optional field, max 1000 characters

- **completed**: Boolean (Default: False)
  - Purpose: Indicates whether the task has been completed
  - Values: True (completed) or False (pending)

### State Transitions
- **Creation**: New tasks are created with `completed = False`
- **Completion**: Task status can be toggled from `False` to `True`
- **Reversion**: Completed task status can be reverted from `True` to `False`

### Validation Rules
- Title must not be empty after trimming whitespace
- Title must be 200 characters or fewer
- Description (if provided) must be 1000 characters or fewer
- ID must be unique within the application session
- ID cannot be negative

## Todo List Collection

### Characteristics
- **Type**: In-memory collection (Python dictionary/list combination)
- **Persistence**: Volatile - data exists only during application runtime
- **Capacity**: Designed to handle up to 100 tasks efficiently

### Operations Supported
- Add new task to collection
- Retrieve task by ID
- Update task details by ID
- Delete task by ID
- List all tasks
- Filter tasks by completion status

### Internal Structure
- Primary storage: Dictionary with ID as key and Task object as value
- Index for fast lookups by ID
- Maintains insertion order for display purposes