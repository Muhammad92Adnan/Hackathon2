"""
Pytest configuration and fixtures for the todo application tests.

This module provides common test fixtures and configuration used across
unit and integration tests.
"""

import pytest
from src.todo_app.services.todo_service import TodoService
from src.todo_app.cli.main_menu import TodoCLI
from src.todo_app.models.task import Task


@pytest.fixture
def empty_service():
    """
    Provide an empty TodoService instance.

    Returns:
        TodoService: A new TodoService with no tasks
    """
    return TodoService()


@pytest.fixture
def service_with_tasks():
    """
    Provide a TodoService instance with sample tasks.

    Returns:
        TodoService: A TodoService with 3 pre-populated tasks
    """
    service = TodoService()
    service.add_task("First Task", "First task description")
    service.add_task("Second Task", "Second task description")
    service.add_task("Third Task", "Third task description")
    return service


@pytest.fixture
def cli_instance():
    """
    Provide a TodoCLI instance for testing.

    Returns:
        TodoCLI: A new TodoCLI instance with empty service
    """
    return TodoCLI()


@pytest.fixture
def sample_task():
    """
    Provide a sample Task instance for testing.

    Returns:
        Task: A sample task with standard attributes
    """
    return Task(
        id=1,
        title="Sample Task",
        description="This is a sample task for testing",
        completed=False
    )


@pytest.fixture
def completed_task():
    """
    Provide a completed Task instance for testing.

    Returns:
        Task: A completed task
    """
    return Task(
        id=2,
        title="Completed Task",
        description="This task is already complete",
        completed=True
    )
