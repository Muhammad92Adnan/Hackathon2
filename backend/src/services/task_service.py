from sqlmodel import Session, select
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate, TaskToggle
from ..models.user import User
from fastapi import HTTPException, status
from datetime import datetime


class TaskService:
    """Service layer for task-related operations."""

    @classmethod
    def create_task(cls, user_id: int, task_create: TaskCreate, db_session: Session) -> Task:
        """
        Create a new task for a user.

        Args:
            user_id: ID of the user who owns the task
            task_create: Task creation request with title and description
            db_session: Database session for the operation

        Returns:
            Created Task object
        """
        db_task = Task(
            user_id=user_id,
            title=task_create.title,
            description=task_create.description or "",
            completed=False
        )
        
        db_session.add(db_task)
        db_session.commit()
        db_session.refresh(db_task)
        
        return db_task

    @classmethod
    def get_tasks_for_user(
        cls, 
        user_id: int, 
        db_session: Session, 
        status_filter: Optional[str] = None
    ) -> List[Task]:
        """
        Get all tasks for a specific user, with optional status filtering.

        Args:
            user_id: ID of the user whose tasks to retrieve
            db_session: Database session for the operation
            status_filter: Optional filter for task status ('all', 'pending', 'completed')

        Returns:
            List of Task objects belonging to the user
        """
        query = select(Task).where(Task.user_id == user_id)
        
        if status_filter == "pending":
            query = query.where(Task.completed == False)
        elif status_filter == "completed":
            query = query.where(Task.completed == True)
        # If status_filter is "all" or None, return all tasks
        
        tasks = db_session.exec(query.order_by(Task.created_at.desc())).all()
        return tasks

    @classmethod
    def get_task_by_id(cls, user_id: int, task_id: int, db_session: Session) -> Task:
        """
        Get a specific task by ID for a user (with ownership validation).

        Args:
            user_id: ID of the user requesting the task
            task_id: ID of the task to retrieve
            db_session: Database session for the operation

        Returns:
            Task object if it belongs to the user

        Raises:
            HTTPException: If task doesn't exist or doesn't belong to user
        """
        task = db_session.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        ).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user"
            )
        
        return task

    @classmethod
    def update_task(
        cls, 
        user_id: int, 
        task_id: int, 
        task_update: TaskUpdate, 
        db_session: Session
    ) -> Task:
        """
        Update a task for a user.

        Args:
            user_id: ID of the user who owns the task
            task_id: ID of the task to update
            task_update: Task update request with fields to update
            db_session: Database session for the operation

        Returns:
            Updated Task object

        Raises:
            HTTPException: If task doesn't exist or doesn't belong to user
        """
        task = cls.get_task_by_id(user_id, task_id, db_session)
        
        # Update fields that are provided in the request
        if task_update.title is not None:
            task.title = task_update.title
        if task_update.description is not None:
            task.description = task_update.description
        if task_update.completed is not None:
            task.completed = task_update.completed
            
        # Update the updated_at timestamp
        task.updated_at = datetime.utcnow()
        
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        return task

    @classmethod
    def toggle_task_completion(
        cls, 
        user_id: int, 
        task_id: int, 
        task_toggle: TaskToggle, 
        db_session: Session
    ) -> Task:
        """
        Toggle the completion status of a task.

        Args:
            user_id: ID of the user who owns the task
            task_id: ID of the task to toggle
            task_toggle: Task toggle request with completion status
            db_session: Database session for the operation

        Returns:
            Updated Task object with new completion status

        Raises:
            HTTPException: If task doesn't exist or doesn't belong to user
        """
        task = cls.get_task_by_id(user_id, task_id, db_session)
        
        task.completed = task_toggle.completed
        task.updated_at = datetime.utcnow()
        
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        return task

    @classmethod
    def delete_task(cls, user_id: int, task_id: int, db_session: Session) -> bool:
        """
        Delete a task for a user.

        Args:
            user_id: ID of the user who owns the task
            task_id: ID of the task to delete
            db_session: Database session for the operation

        Returns:
            True if task was deleted, False otherwise

        Raises:
            HTTPException: If task doesn't exist or doesn't belong to user
        """
        task = cls.get_task_by_id(user_id, task_id, db_session)
        
        db_session.delete(task)
        db_session.commit()
        
        return True