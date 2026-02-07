"""
Input validation utilities for the todo application.

This module provides validation functions for user inputs including
title validation and ID validation.
"""

from typing import Optional


def validate_title(title: str) -> tuple[bool, Optional[str]]:
    """
    Validate a task title.

    Args:
        title: The title string to validate

    Returns:
        A tuple of (is_valid: bool, error_message: Optional[str])
        If valid, returns (True, None)
        If invalid, returns (False, error_message)
    """
    if not title:
        return False, "Title cannot be empty"

    stripped_title = title.strip()
    if not stripped_title:
        return False, "Title cannot be only whitespace"

    if len(stripped_title) > 200:
        return False, "Title cannot exceed 200 characters"

    return True, None


def validate_description(description: str) -> tuple[bool, Optional[str]]:
    """
    Validate a task description.

    Args:
        description: The description string to validate

    Returns:
        A tuple of (is_valid: bool, error_message: Optional[str])
        If valid, returns (True, None)
        If invalid, returns (False, error_message)
    """
    if description and len(description) > 1000:
        return False, "Description cannot exceed 1000 characters"

    return True, None


def validate_task_id(task_id_str: str, max_id: int = 0) -> tuple[bool, Optional[int], Optional[str]]:
    """
    Validate and convert a task ID string.

    Args:
        task_id_str: The ID string to validate
        max_id: Maximum valid ID (optional, for range checking)

    Returns:
        A tuple of (is_valid: bool, task_id: Optional[int], error_message: Optional[str])
        If valid, returns (True, task_id, None)
        If invalid, returns (False, None, error_message)
    """
    if not task_id_str:
        return False, None, "Task ID cannot be empty"

    try:
        task_id = int(task_id_str.strip())
    except ValueError:
        return False, None, "Task ID must be a valid number"

    if task_id < 0:
        return False, None, "Task ID cannot be negative"

    if max_id > 0 and task_id > max_id:
        return False, None, f"Task ID {task_id} does not exist (max ID: {max_id})"

    return True, task_id, None


def get_user_input(prompt: str, allow_empty: bool = False) -> Optional[str]:
    """
    Get user input with optional empty validation.

    Args:
        prompt: The prompt to display to the user
        allow_empty: Whether to allow empty input (default: False)

    Returns:
        The user's input string, or None if empty and not allowed
    """
    user_input = input(prompt).strip()

    if not allow_empty and not user_input:
        return None

    return user_input
