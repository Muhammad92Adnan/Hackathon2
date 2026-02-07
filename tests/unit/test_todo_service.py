"""Unit tests for the TodoService."""

import pytest
from src.todo_app.services.todo_service import TodoService
from src.todo_app.models.task import Task


class TestAddTask:
    """Test adding tasks to the service."""

    def test_add_task_with_title_only(self):
        """Test adding a task with only a title."""
        service = TodoService()

        task = service.add_task("Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False

    def test_add_task_with_title_and_description(self):
        """Test adding a task with title and description."""
        service = TodoService()

        task = service.add_task("Test Task", "Test Description")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_add_multiple_tasks_increments_id(self):
        """Test that adding multiple tasks increments the ID."""
        service = TodoService()

        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_with_invalid_title_fails(self):
        """Test that adding a task with invalid title raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError):
            service.add_task("")


class TestGetTask:
    """Test retrieving tasks from the service."""

    def test_get_existing_task(self):
        """Test retrieving an existing task."""
        service = TodoService()
        added_task = service.add_task("Test Task")

        retrieved_task = service.get_task(1)

        assert retrieved_task is not None
        assert retrieved_task.id == added_task.id
        assert retrieved_task.title == added_task.title

    def test_get_nonexistent_task_returns_none(self):
        """Test retrieving a nonexistent task returns None."""
        service = TodoService()

        task = service.get_task(999)

        assert task is None


class TestListTasks:
    """Test listing all tasks."""

    def test_list_tasks_when_empty(self):
        """Test listing tasks when service is empty."""
        service = TodoService()

        tasks = service.list_tasks()

        assert tasks == []

    def test_list_tasks_returns_all_tasks(self):
        """Test that list_tasks returns all added tasks."""
        service = TodoService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")

        tasks = service.list_tasks()

        assert len(tasks) == 3
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"
        assert tasks[2].title == "Task 3"

    def test_list_tasks_returns_sorted_by_id(self):
        """Test that list_tasks returns tasks sorted by ID."""
        service = TodoService()
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")

        # Delete middle task
        service.delete_task(2)

        tasks = service.list_tasks()

        assert len(tasks) == 2
        assert tasks[0].id == 1
        assert tasks[1].id == 3


class TestUpdateTask:
    """Test updating tasks."""

    def test_update_task_title(self):
        """Test updating only the title of a task."""
        service = TodoService()
        service.add_task("Original Title", "Original Description")

        success = service.update_task(1, title="New Title")

        assert success is True
        task = service.get_task(1)
        assert task.title == "New Title"
        assert task.description == "Original Description"

    def test_update_task_description(self):
        """Test updating only the description of a task."""
        service = TodoService()
        service.add_task("Original Title", "Original Description")

        success = service.update_task(1, description="New Description")

        assert success is True
        task = service.get_task(1)
        assert task.title == "Original Title"
        assert task.description == "New Description"

    def test_update_task_both_fields(self):
        """Test updating both title and description."""
        service = TodoService()
        service.add_task("Original Title", "Original Description")

        success = service.update_task(1, title="New Title", description="New Description")

        assert success is True
        task = service.get_task(1)
        assert task.title == "New Title"
        assert task.description == "New Description"

    def test_update_nonexistent_task_returns_false(self):
        """Test updating a nonexistent task returns False."""
        service = TodoService()

        success = service.update_task(999, title="New Title")

        assert success is False


class TestDeleteTask:
    """Test deleting tasks."""

    def test_delete_existing_task(self):
        """Test deleting an existing task."""
        service = TodoService()
        service.add_task("Task to Delete")

        success = service.delete_task(1)

        assert success is True
        assert service.get_task(1) is None
        assert len(service.list_tasks()) == 0

    def test_delete_nonexistent_task_returns_false(self):
        """Test deleting a nonexistent task returns False."""
        service = TodoService()

        success = service.delete_task(999)

        assert success is False


class TestToggleComplete:
    """Test toggling task completion."""

    def test_toggle_complete_existing_task(self):
        """Test toggling completion of an existing task."""
        service = TodoService()
        service.add_task("Test Task")

        success = service.toggle_complete(1)

        assert success is True
        task = service.get_task(1)
        assert task.completed is True

    def test_toggle_complete_twice_returns_to_original(self):
        """Test toggling completion twice returns to original state."""
        service = TodoService()
        service.add_task("Test Task")

        service.toggle_complete(1)
        service.toggle_complete(1)

        task = service.get_task(1)
        assert task.completed is False

    def test_toggle_complete_nonexistent_task_returns_false(self):
        """Test toggling completion of nonexistent task returns False."""
        service = TodoService()

        success = service.toggle_complete(999)

        assert success is False


class TestTaskCounts:
    """Test task counting methods."""

    def test_get_task_count_when_empty(self):
        """Test getting task count when service is empty."""
        service = TodoService()

        count = service.get_task_count()

        assert count == 0

    def test_get_task_count_with_tasks(self):
        """Test getting task count with multiple tasks."""
        service = TodoService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")

        count = service.get_task_count()

        assert count == 3

    def test_get_completed_count(self):
        """Test getting count of completed tasks."""
        service = TodoService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")

        service.toggle_complete(1)
        service.toggle_complete(3)

        completed_count = service.get_completed_count()

        assert completed_count == 2

    def test_get_pending_count(self):
        """Test getting count of pending tasks."""
        service = TodoService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")

        service.toggle_complete(1)

        pending_count = service.get_pending_count()

        assert pending_count == 2

    def test_counts_after_deletion(self):
        """Test that counts are updated after task deletion."""
        service = TodoService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")

        service.toggle_complete(1)
        service.delete_task(2)

        assert service.get_task_count() == 2
        assert service.get_completed_count() == 1
        assert service.get_pending_count() == 1
