# Claude Code Instructions - Phase I Console Todo Application

## Project Overview

This is a Python 3.13+ console application implementing a todo list with in-memory storage and CRUD operations.

## Development Workflow

This project follows Spec-Driven Development (SDD) using Claude Code:

1. **Specification** (`specs/001-console-todo/spec.md`) - Feature requirements
2. **Plan** (`specs/001-console-todo/plan.md`) - Implementation strategy
3. **Tasks** (`specs/001-console-todo/tasks.md`) - Detailed task breakdown
4. **Implementation** - Generated via `/sp.implement`

## Project Structure

```
src/todo_app/          # Main application package
├── models/            # Data models (Task)
├── services/          # Business logic (TodoService)
├── cli/               # CLI interface (TodoCLI)
├── utils/             # Validators and helpers
└── __main__.py        # Application entry point

tests/                 # Test suite
├── unit/              # Unit tests for models and services
└── integration/       # Integration tests for CLI flows

specs/001-console-todo/ # Specification documents
├── spec.md            # Feature specification
├── plan.md            # Implementation plan
├── tasks.md           # Task breakdown
├── data-model.md      # Data model documentation
├── research.md        # Technical decisions
└── quickstart.md      # Quick start guide
```

## Running the Application

```bash
# Execute the todo app
python -m src.todo_app
```

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## Key Components

### Task Model (`src/todo_app/models/task.py`)
- Dataclass with validation
- Attributes: id, title, description, completed
- Methods: toggle_complete(), update()

### TodoService (`src/todo_app/services/todo_service.py`)
- In-memory storage using Python dict
- CRUD operations: add_task, get_task, list_tasks, update_task, delete_task, toggle_complete
- Task counting methods

### TodoCLI (`src/todo_app/cli/main_menu.py`)
- Interactive menu system
- User flows for all operations
- Input validation and error handling

## Code Standards

- **PEP 8** compliance
- **Type hints** on all functions
- **Docstrings** for all public APIs
- **Validation** at model and service layers
- **Error handling** with user-friendly messages

## Making Changes

When adding features or fixing bugs:

1. Update specification (`specs/001-console-todo/spec.md`)
2. Regenerate plan if needed (`/sp.plan`)
3. Regenerate tasks (`/sp.tasks`)
4. Implement changes (`/sp.implement`)
5. Run tests to verify
6. Update documentation

## Testing Philosophy

- **Unit tests**: Test individual components in isolation
- **Integration tests**: Test CLI flows end-to-end
- **TDD approach**: Write tests first, ensure they fail, then implement

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python -m src.todo_app

# Run tests
python -m pytest tests/ -v

# Format code (if using black)
black src/ tests/

# Type check (if using mypy)
mypy src/
```

## Notes

- Data is stored in memory only - lost on application exit
- No persistence layer (Phase I constraint)
- Task IDs auto-increment from 1
- Title validation: 1-200 characters, non-empty
- Description validation: 0-1000 characters
