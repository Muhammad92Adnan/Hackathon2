"""
Entry point for the todo application.

This module provides the main entry point when running the application
as a module using: python -m src.todo_app
"""

from .cli.main_menu import TodoCLI


def main() -> None:
    """Main entry point for the application."""
    try:
        cli = TodoCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        print("Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please report this issue.")


if __name__ == "__main__":
    main()
