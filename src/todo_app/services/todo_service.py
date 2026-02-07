"""
Todo service for managing tasks in memory.

This module provides the core business logic for CRUD operations
on todo tasks with in-memory storage.
"""

from typing import Dict, List, Optional
from ..models.task import Task


class TodoService:
    """
    Service class for managing todo tasks in memory.

    Attributes:
        _tasks: Dictionary storing tasks with ID as key
        _next_id: Counter for generating unique task IDs
    """

    def __init__(self) -> None:
        """Initialize the todo service with empty in-memory storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task to the todo list.

        Args:
            title: The title of the task
            description: Optional description of the task

        Returns:
            The newly created Task object

        Raises:
            ValueError: If title is invalid
        """
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        return self._tasks.get(task_id)

    def list_tasks(self) -> List[Task]:
        """
        Get all tasks in the todo list.

        Returns:
            List of all Task objects, ordered by ID
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None) -> bool:
        """
        Update an existing task.

        Args:
            task_id: The ID of the task to update
            title: New title for the task (if provided)
            description: New description for the task (if provided)

        Returns:
            True if task was updated, False if task not found

        Raises:
            ValueError: If new title or description is invalid
        """
        task = self.get_task(task_id)
        if task is None:
            return False

        task.update(title=title, description=description)
        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task from the todo list.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if task was deleted, False if task not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def toggle_complete(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            True if task was toggled, False if task not found
        """
        task = self.get_task(task_id)
        if task is None:
            return False

        task.toggle_complete()
        return True

    def get_task_count(self) -> int:
        """
        Get the total number of tasks.

        Returns:
            The total count of tasks
        """
        return len(self._tasks)

    def get_completed_count(self) -> int:
        """
        Get the count of completed tasks.

        Returns:
            The count of completed tasks
        """
        return sum(1 for task in self._tasks.values() if task.completed)

    def get_pending_count(self) -> int:
        """
        Get the count of pending (incomplete) tasks.

        Returns:
            The count of pending tasks
        """
        return sum(1 for task in self._tasks.values() if not task.completed)
