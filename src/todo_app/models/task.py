"""
Task model for the todo application.

This module defines the Task entity with attributes for ID, title,
description, and completion status.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    """
    Represents a todo task item.

    Attributes:
        id: Unique identifier for the task (auto-assigned)
        title: Brief description or name of the task (required)
        description: Detailed information about the task (optional)
        completed: Indicates whether the task has been completed (default: False)
    """

    id: int
    title: str
    description: Optional[str] = ""
    completed: bool = False

    def __post_init__(self) -> None:
        """
        Validate task attributes after initialization.

        Raises:
            ValueError: If title is empty or whitespace-only
            ValueError: If title exceeds 200 characters
            ValueError: If description exceeds 1000 characters
            ValueError: If ID is negative
        """
        # Validate title
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")

        if len(self.title) > 200:
            raise ValueError("Task title cannot exceed 200 characters")

        # Validate description
        if self.description and len(self.description) > 1000:
            raise ValueError("Task description cannot exceed 1000 characters")

        # Validate ID
        if self.id < 0:
            raise ValueError("Task ID cannot be negative")

    def toggle_complete(self) -> None:
        """Toggle the completion status of the task."""
        self.completed = not self.completed

    def update(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        """
        Update task details.

        Args:
            title: New title for the task (if provided)
            description: New description for the task (if provided)

        Raises:
            ValueError: If new title is empty or exceeds length limits
            ValueError: If new description exceeds length limits
        """
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Task title cannot be empty")
            if len(title) > 200:
                raise ValueError("Task title cannot exceed 200 characters")
            self.title = title

        if description is not None:
            if len(description) > 1000:
                raise ValueError("Task description cannot exceed 1000 characters")
            self.description = description

    def __str__(self) -> str:
        """Return a string representation of the task."""
        status = "[X]" if self.completed else "[ ]"
        desc_preview = (
            f" - {self.description[:50]}..." if len(self.description) > 50
            else f" - {self.description}" if self.description
            else ""
        )
        return f"{status} #{self.id}: {self.title}{desc_preview}"
