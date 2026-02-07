"""Unit tests for the Task model."""

import pytest
from src.todo_app.models.task import Task


class TestTaskCreation:
    """Test task creation and initialization."""

    def test_create_task_with_all_fields(self):
        """Test creating a task with all fields specified."""
        task = Task(id=1, title="Test Task", description="Test Description", completed=False)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_create_task_with_minimal_fields(self):
        """Test creating a task with only required fields."""
        task = Task(id=1, title="Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False

    def test_create_task_with_empty_title_fails(self):
        """Test that creating a task with empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(id=1, title="")

    def test_create_task_with_whitespace_title_fails(self):
        """Test that creating a task with whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(id=1, title="   ")

    def test_create_task_with_long_title_fails(self):
        """Test that creating a task with title > 200 chars raises ValueError."""
        long_title = "a" * 201
        with pytest.raises(ValueError, match="Task title cannot exceed 200 characters"):
            Task(id=1, title=long_title)

    def test_create_task_with_long_description_fails(self):
        """Test that creating a task with description > 1000 chars raises ValueError."""
        long_desc = "a" * 1001
        with pytest.raises(ValueError, match="Task description cannot exceed 1000 characters"):
            Task(id=1, title="Test", description=long_desc)

    def test_create_task_with_negative_id_fails(self):
        """Test that creating a task with negative ID raises ValueError."""
        with pytest.raises(ValueError, match="Task ID cannot be negative"):
            Task(id=-1, title="Test Task")


class TestTaskToggleComplete:
    """Test task completion toggling."""

    def test_toggle_complete_from_false_to_true(self):
        """Test toggling completion status from incomplete to complete."""
        task = Task(id=1, title="Test Task", completed=False)

        task.toggle_complete()

        assert task.completed is True

    def test_toggle_complete_from_true_to_false(self):
        """Test toggling completion status from complete to incomplete."""
        task = Task(id=1, title="Test Task", completed=True)

        task.toggle_complete()

        assert task.completed is False

    def test_toggle_complete_multiple_times(self):
        """Test toggling completion status multiple times."""
        task = Task(id=1, title="Test Task")

        task.toggle_complete()
        assert task.completed is True

        task.toggle_complete()
        assert task.completed is False

        task.toggle_complete()
        assert task.completed is True


class TestTaskUpdate:
    """Test task update functionality."""

    def test_update_title(self):
        """Test updating only the title."""
        task = Task(id=1, title="Original Title", description="Original Description")

        task.update(title="New Title")

        assert task.title == "New Title"
        assert task.description == "Original Description"

    def test_update_description(self):
        """Test updating only the description."""
        task = Task(id=1, title="Original Title", description="Original Description")

        task.update(description="New Description")

        assert task.title == "Original Title"
        assert task.description == "New Description"

    def test_update_both_title_and_description(self):
        """Test updating both title and description."""
        task = Task(id=1, title="Original Title", description="Original Description")

        task.update(title="New Title", description="New Description")

        assert task.title == "New Title"
        assert task.description == "New Description"

    def test_update_with_empty_title_fails(self):
        """Test that updating with empty title raises ValueError."""
        task = Task(id=1, title="Original Title")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task.update(title="")

    def test_update_with_long_title_fails(self):
        """Test that updating with title > 200 chars raises ValueError."""
        task = Task(id=1, title="Original Title")
        long_title = "a" * 201

        with pytest.raises(ValueError, match="Task title cannot exceed 200 characters"):
            task.update(title=long_title)

    def test_update_with_long_description_fails(self):
        """Test that updating with description > 1000 chars raises ValueError."""
        task = Task(id=1, title="Original Title")
        long_desc = "a" * 1001

        with pytest.raises(ValueError, match="Task description cannot exceed 1000 characters"):
            task.update(description=long_desc)


class TestTaskStringRepresentation:
    """Test task string representation."""

    def test_str_incomplete_task_without_description(self):
        """Test string representation of incomplete task without description."""
        task = Task(id=1, title="Test Task")

        result = str(task)

        assert result == "[ ] #1: Test Task"

    def test_str_complete_task_without_description(self):
        """Test string representation of complete task without description."""
        task = Task(id=1, title="Test Task", completed=True)

        result = str(task)

        assert result == "[X] #1: Test Task"

    def test_str_task_with_short_description(self):
        """Test string representation of task with short description."""
        task = Task(id=1, title="Test Task", description="Short description")

        result = str(task)

        assert result == "[ ] #1: Test Task - Short description"

    def test_str_task_with_long_description(self):
        """Test string representation of task with long description (truncated)."""
        long_desc = "This is a very long description that exceeds fifty characters"
        task = Task(id=1, title="Test Task", description=long_desc)

        result = str(task)

        assert result.startswith("[ ] #1: Test Task - This is a very long description that exceeds fifty...")
        assert len(result) <= len("[ ] #1: Test Task - ") + 53  # 50 chars + "..."
