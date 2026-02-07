"""
Main menu CLI for the todo application.

This module provides the interactive command-line interface for
managing todo tasks.
"""

from typing import Optional
from ..services.todo_service import TodoService
from ..utils.validators import validate_title, validate_description, validate_task_id, get_user_input


class TodoCLI:
    """
    Command-line interface for the todo application.

    Attributes:
        service: The TodoService instance for managing tasks
    """

    def __init__(self) -> None:
        """Initialize the CLI with a new TodoService."""
        self.service = TodoService()

    def display_menu(self) -> None:
        """Display the main menu options."""
        print("\n" + "=" * 50)
        print("TODO LIST APPLICATION")
        print("=" * 50)
        print("1. Add Task")
        print("2. View Task List")
        print("3. Mark Task as Complete")
        print("4. Update Task")
        print("5. Delete Task")
        print("6. Exit")
        print("=" * 50)

    def add_task_flow(self) -> None:
        """Handle the add task user flow."""
        print("\n--- Add New Task ---")

        # Get title
        while True:
            title = get_user_input("Enter task title: ")
            if title is None:
                print("Error: Title cannot be empty")
                continue

            is_valid, error = validate_title(title)
            if not is_valid:
                print(f"Error: {error}")
                continue

            break

        # Get description
        description = get_user_input("Enter task description (optional): ", allow_empty=True) or ""

        is_valid, error = validate_description(description)
        if not is_valid:
            print(f"Error: {error}")
            return

        # Add task
        try:
            task = self.service.add_task(title, description)
            print(f"\n[OK] Task added successfully: {task}")
        except ValueError as e:
            print(f"\nError adding task: {e}")

    def view_tasks_flow(self) -> None:
        """Handle the view tasks user flow."""
        print("\n--- Task List ---")

        tasks = self.service.list_tasks()

        if not tasks:
            print("No tasks found. Add a task to get started!")
            return

        print(f"\nTotal: {self.service.get_task_count()} tasks | "
              f"Completed: {self.service.get_completed_count()} | "
              f"Pending: {self.service.get_pending_count()}")
        print()

        for task in tasks:
            print(task)

    def toggle_complete_flow(self) -> None:
        """Handle the mark complete user flow."""
        print("\n--- Mark Task as Complete ---")

        # Show current tasks
        tasks = self.service.list_tasks()
        if not tasks:
            print("No tasks available.")
            return

        for task in tasks:
            print(task)

        # Get task ID
        task_id_str = get_user_input("\nEnter task ID to toggle completion: ")
        if task_id_str is None:
            print("Error: Task ID cannot be empty")
            return

        is_valid, task_id, error = validate_task_id(task_id_str)
        if not is_valid:
            print(f"Error: {error}")
            return

        # Toggle task
        success = self.service.toggle_complete(task_id)
        if success:
            task = self.service.get_task(task_id)
            status = "completed" if task.completed else "incomplete"
            print(f"\n[OK] Task #{task_id} marked as {status}")
        else:
            print(f"\nError: Task #{task_id} not found")

    def update_task_flow(self) -> None:
        """Handle the update task user flow."""
        print("\n--- Update Task ---")

        # Show current tasks
        tasks = self.service.list_tasks()
        if not tasks:
            print("No tasks available.")
            return

        for task in tasks:
            print(task)

        # Get task ID
        task_id_str = get_user_input("\nEnter task ID to update: ")
        if task_id_str is None:
            print("Error: Task ID cannot be empty")
            return

        is_valid, task_id, error = validate_task_id(task_id_str)
        if not is_valid:
            print(f"Error: {error}")
            return

        # Check if task exists
        task = self.service.get_task(task_id)
        if task is None:
            print(f"\nError: Task #{task_id} not found")
            return

        print(f"\nCurrent task: {task}")

        # Get new title
        new_title = get_user_input("\nEnter new title (or press Enter to keep current): ", allow_empty=True)
        if new_title:
            is_valid, error = validate_title(new_title)
            if not is_valid:
                print(f"Error: {error}")
                return
        else:
            new_title = None

        # Get new description
        new_desc = get_user_input("Enter new description (or press Enter to keep current): ", allow_empty=True)
        if new_desc == "":
            new_desc = None

        if new_desc is not None:
            is_valid, error = validate_description(new_desc)
            if not is_valid:
                print(f"Error: {error}")
                return

        # Update task
        try:
            success = self.service.update_task(task_id, title=new_title, description=new_desc)
            if success:
                print(f"\n[OK] Task #{task_id} updated successfully")
                print(f"Updated task: {self.service.get_task(task_id)}")
            else:
                print(f"\nError: Task #{task_id} not found")
        except ValueError as e:
            print(f"\nError updating task: {e}")

    def delete_task_flow(self) -> None:
        """Handle the delete task user flow."""
        print("\n--- Delete Task ---")

        # Show current tasks
        tasks = self.service.list_tasks()
        if not tasks:
            print("No tasks available.")
            return

        for task in tasks:
            print(task)

        # Get task ID
        task_id_str = get_user_input("\nEnter task ID to delete: ")
        if task_id_str is None:
            print("Error: Task ID cannot be empty")
            return

        is_valid, task_id, error = validate_task_id(task_id_str)
        if not is_valid:
            print(f"Error: {error}")
            return

        # Confirm deletion
        task = self.service.get_task(task_id)
        if task is None:
            print(f"\nError: Task #{task_id} not found")
            return

        print(f"\nTask to delete: {task}")
        confirm = get_user_input("Are you sure you want to delete this task? (yes/no): ", allow_empty=True)

        if confirm and confirm.lower() in ['yes', 'y']:
            success = self.service.delete_task(task_id)
            if success:
                print(f"\n[OK] Task #{task_id} deleted successfully")
            else:
                print(f"\nError: Task #{task_id} not found")
        else:
            print("\nDeletion cancelled")

    def run(self) -> None:
        """Run the main application loop."""
        print("\nWelcome to the Todo List Application!")

        while True:
            self.display_menu()

            choice = get_user_input("\nEnter your choice (1-6): ")

            if choice == "1":
                self.add_task_flow()
            elif choice == "2":
                self.view_tasks_flow()
            elif choice == "3":
                self.toggle_complete_flow()
            elif choice == "4":
                self.update_task_flow()
            elif choice == "5":
                self.delete_task_flow()
            elif choice == "6":
                print("\nThank you for using the Todo List Application!")
                print("Goodbye!")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 6.")
