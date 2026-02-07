# Phase I Console Todo Application

A simple command-line todo list application with in-memory storage, supporting basic CRUD operations.

## Features

- ✅ Add tasks with title and description
- ✅ View all tasks with completion status
- ✅ Mark tasks as complete/incomplete
- ✅ Update existing task details
- ✅ Delete tasks by ID
- ✅ Interactive menu-driven interface
- ✅ Input validation and error handling

## Requirements

- Python 3.13+ or compatible version
- pytest (for running tests)

## Installation

### Using pip

```bash
# Install dependencies
pip install -r requirements.txt
```

### Using uv (recommended)

```bash
# Install uv if you haven't already
pip install uv

# Install dependencies
uv pip install -r requirements.txt
```

## Running the Application

```bash
# Run as a module
python -m src.todo_app
```

The application will display an interactive menu with the following options:

1. **Add Task** - Create a new todo item
2. **View Task List** - Display all tasks with status
3. **Mark Task as Complete** - Toggle completion status
4. **Update Task** - Modify task details
5. **Delete Task** - Remove a task
6. **Exit** - Close the application

## Development

### Project Structure

```
src/
├── todo_app/
│   ├── __init__.py
│   ├── models/
│   │   └── task.py           # Task entity
│   ├── services/
│   │   └── todo_service.py   # Business logic
│   ├── cli/
│   │   └── main_menu.py      # CLI interface
│   ├── utils/
│   │   └── validators.py     # Input validators
│   └── __main__.py           # Entry point
tests/
├── unit/                      # Unit tests
└── integration/               # Integration tests
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run unit tests only
python -m pytest tests/unit/ -v

# Run integration tests only
python -m pytest tests/integration/ -v

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Code Quality

This project follows:
- **PEP 8** style guidelines
- **Type hints** for all function parameters and return values
- **Docstrings** for all public classes and methods
- **Comprehensive testing** with 54 passing tests

## Architecture

The application uses a layered architecture:

- **Models**: Data entities with validation logic
- **Services**: Business logic and in-memory storage
- **CLI**: User interface and menu system
- **Utils**: Shared validation utilities

All data is stored in memory and will be lost when the application closes.

## Limitations (Phase I)

- No persistent storage (data is lost on exit)
- No database (Phase II feature)
- No web interface (Phase II feature)
- No authentication (Phase II feature)
- Single-user console application

## Future Phases

- **Phase II**: Web application with PostgreSQL database
- **Phase III**: Chatbot interface with OpenAI integration
- **Phase IV**: Kubernetes deployment
- **Phase V**: Cloud deployment with event-driven architecture

## License

This is a Phase I implementation for the Hackathon II - Todo App Evolution project.
