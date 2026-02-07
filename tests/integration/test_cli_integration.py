"""Integration tests for the CLI."""

import pytest
from io import StringIO
from unittest.mock import patch
from src.todo_app.cli.main_menu import TodoCLI


class TestAddTaskIntegration:
    """Integration tests for adding tasks through the CLI."""

    @patch('builtins.input', side_effect=["Test Task", "Test Description"])
    def test_add_task_with_description_success(self, mock_input):
        """Test adding a task with title and description through CLI."""
        cli = TodoCLI()

        # Capture stdout
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.add_task_flow()
            output = fake_out.getvalue()

        # Verify task was added
        tasks = cli.service.list_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Test Task"
        assert tasks[0].description == "Test Description"
        assert "Task added successfully" in output

    @patch('builtins.input', side_effect=["", "Valid Task", ""])
    def test_add_task_with_empty_title_retry(self, mock_input):
        """Test adding a task with empty title requires retry."""
        cli = TodoCLI()

        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.add_task_flow()
            output = fake_out.getvalue()

        # Verify error message and successful retry
        assert "Title cannot be empty" in output
        tasks = cli.service.list_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Valid Task"


class TestViewTasksIntegration:
    """Integration tests for viewing tasks through the CLI."""

    def test_view_tasks_when_empty(self):
        """Test viewing tasks when no tasks exist."""
        cli = TodoCLI()

        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.view_tasks_flow()
            output = fake_out.getvalue()

        assert "No tasks found" in output

    def test_view_tasks_with_multiple_tasks(self):
        """Test viewing tasks when multiple tasks exist."""
        cli = TodoCLI()
        cli.service.add_task("Task 1", "Description 1")
        cli.service.add_task("Task 2", "Description 2")
        cli.service.toggle_complete(1)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.view_tasks_flow()
            output = fake_out.getvalue()

        assert "Total: 2 tasks" in output
        assert "Completed: 1" in output
        assert "Pending: 1" in output
        assert "Task 1" in output
        assert "Task 2" in output


class TestToggleCompleteIntegration:
    """Integration tests for toggling task completion through the CLI."""

    @patch('builtins.input', return_value="1")
    def test_toggle_complete_existing_task(self, mock_input):
        """Test toggling completion of an existing task."""
        cli = TodoCLI()
        cli.service.add_task("Test Task")

        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.toggle_complete_flow()
            output = fake_out.getvalue()

        assert "marked as completed" in output
        task = cli.service.get_task(1)
        assert task.completed is True

    @patch('builtins.input', return_value="999")
    def test_toggle_complete_nonexistent_task(self, mock_input):
        """Test toggling completion of nonexistent task shows error."""
        cli = TodoCLI()
        cli.service.add_task("Test Task")

        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.toggle_complete_flow()
            output = fake_out.getvalue()

        assert "not found" in output


class TestUpdateTaskIntegration:
    """Integration tests for updating tasks through the CLI."""

    @patch('builtins.input', side_effect=["1", "Updated Title", "Updated Description"])
    def test_update_task_both_fields(self, mock_input):
        """Test updating both title and description of a task."""
        cli = TodoCLI()
        cli.service.add_task("Original Title", "Original Description")

        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.update_task_flow()
            output = fake_out.getvalue()

        assert "updated successfully" in output
        task = cli.service.get_task(1)
        assert task.title == "Updated Title"
        assert task.description == "Updated Description"

    @patch('builtins.input', side_effect=["1", "", "New Description"])
    def test_update_task_description_only(self, mock_input):
        """Test updating only description keeps original title."""
        cli = TodoCLI()
        cli.service.add_task("Original Title", "Original Description")

        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.update_task_flow()
            output = fake_out.getvalue()

        task = cli.service.get_task(1)
        assert task.title == "Original Title"
        assert task.description == "New Description"


class TestDeleteTaskIntegration:
    """Integration tests for deleting tasks through the CLI."""

    @patch('builtins.input', side_effect=["1", "yes"])
    def test_delete_task_with_confirmation(self, mock_input):
        """Test deleting a task with user confirmation."""
        cli = TodoCLI()
        cli.service.add_task("Task to Delete")

        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.delete_task_flow()
            output = fake_out.getvalue()

        assert "deleted successfully" in output
        assert cli.service.get_task(1) is None
        assert len(cli.service.list_tasks()) == 0

    @patch('builtins.input', side_effect=["1", "no"])
    def test_delete_task_cancelled(self, mock_input):
        """Test cancelling task deletion."""
        cli = TodoCLI()
        cli.service.add_task("Task to Keep")

        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.delete_task_flow()
            output = fake_out.getvalue()

        assert "cancelled" in output
        assert cli.service.get_task(1) is not None
        assert len(cli.service.list_tasks()) == 1

    @patch('builtins.input', side_effect=["999"])
    def test_delete_nonexistent_task(self, mock_input):
        """Test deleting nonexistent task shows error."""
        cli = TodoCLI()

        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.delete_task_flow()
            output = fake_out.getvalue()

        assert "not found" in output or "No tasks available" in output
