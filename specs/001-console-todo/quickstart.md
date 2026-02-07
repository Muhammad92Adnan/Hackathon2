# Quickstart Guide: Phase I Console Todo Application

## Prerequisites
- Python 3.13+ installed
- uv package manager installed

## Setup

1. Clone the repository:
```bash
git clone <repo-url>
cd <repo-directory>
```

2. Install dependencies using uv:
```bash
uv sync
```

Or if starting fresh:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

## Running the Application

Start the application:
```bash
python -m src.todo_app
```

Or alternatively:
```bash
python src/todo_app/__main__.py
```

## Using the Application

The application presents an interactive menu system:

1. **Add Task**: Creates a new todo item with title and description
2. **View Task List**: Displays all tasks with their status (completed/incomplete)
3. **Update Task**: Modifies existing task details (title/description)
4. **Delete Task**: Removes a task by ID
5. **Mark as Complete**: Toggles completion status of a task
6. **Exit**: Closes the application

## Development

### Running Tests
```bash
pytest tests/
```

### Running Specific Test Groups
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/
```

### Adding Dependencies
When adding new dependencies, update pyproject.toml and run:
```bash
uv lock
```

## Troubleshooting

- **Import errors**: Ensure virtual environment is activated and dependencies are installed
- **Module not found**: Run the application from the repository root directory
- **Permission errors**: Check file permissions on executable files