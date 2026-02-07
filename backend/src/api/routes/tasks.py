from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from ..db.database import get_session
from ..models.task import TaskCreate, TaskRead, TaskUpdate, TaskToggle
from ..models.user import UserRead
from ..services.task_service import TaskService
from ..api.middleware.jwt_auth import get_current_user
from typing import List, Optional


router = APIRouter()


@router.get("/{user_id}/tasks", response_model=List[TaskRead])
async def get_tasks(
    user_id: int,
    current_user: UserRead = Depends(get_current_user),
    status_filter: Optional[str] = Query(None, alias="status", regex="^(all|pending|completed)$"),
    db: Session = Depends(get_session)
):
    """
    Get all tasks for a specific user with optional status filtering.
    
    Args:
        user_id: ID of the user whose tasks to retrieve
        current_user: Currently authenticated user (from JWT)
        status_filter: Optional filter for task status ('all', 'pending', 'completed')
        db: Database session dependency
    
    Returns:
        List of tasks for the user
    
    Raises:
        HTTPException: If user_id in path doesn't match authenticated user
    """
    # Verify that the user_id in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )
    
    tasks = TaskService.get_tasks_for_user(user_id, db, status_filter)
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskRead)
async def create_task(
    user_id: int,
    task_create: TaskCreate,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Create a new task for a user.
    
    Args:
        user_id: ID of the user who will own the task
        task_create: Task creation request with title and description
        current_user: Currently authenticated user (from JWT)
        db: Database session dependency
    
    Returns:
        Created task object
    
    Raises:
        HTTPException: If user_id in path doesn't match authenticated user
    """
    # Verify that the user_id in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )
    
    db_task = TaskService.create_task(user_id, task_create, db)
    return db_task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskRead)
async def get_task(
    user_id: int,
    task_id: int,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Get a specific task by ID for a user.
    
    Args:
        user_id: ID of the user requesting the task
        task_id: ID of the task to retrieve
        current_user: Currently authenticated user (from JWT)
        db: Database session dependency
    
    Returns:
        Requested task object
    
    Raises:
        HTTPException: If user_id in path doesn't match authenticated user or task not found
    """
    # Verify that the user_id in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )
    
    task = TaskService.get_task_by_id(user_id, task_id, db)
    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    user_id: int,
    task_id: int,
    task_update: TaskUpdate,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Update a task for a user.
    
    Args:
        user_id: ID of the user who owns the task
        task_id: ID of the task to update
        task_update: Task update request with fields to update
        current_user: Currently authenticated user (from JWT)
        db: Database session dependency
    
    Returns:
        Updated task object
    
    Raises:
        HTTPException: If user_id in path doesn't match authenticated user or task not found
    """
    # Verify that the user_id in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )
    
    updated_task = TaskService.update_task(user_id, task_id, task_update, db)
    return updated_task


@router.patch("/{user_id}/tasks/{task_id}/toggle", response_model=TaskRead)
async def toggle_task_completion(
    user_id: int,
    task_id: int,
    task_toggle: TaskToggle,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task.
    
    Args:
        user_id: ID of the user who owns the task
        task_id: ID of the task to toggle
        task_toggle: Task toggle request with completion status
        current_user: Currently authenticated user (from JWT)
        db: Database session dependency
    
    Returns:
        Updated task object with new completion status
    
    Raises:
        HTTPException: If user_id in path doesn't match authenticated user or task not found
    """
    # Verify that the user_id in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to toggle this task"
        )
    
    updated_task = TaskService.toggle_task_completion(user_id, task_id, task_toggle, db)
    return updated_task


@router.delete("/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: int,
    task_id: int,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Delete a task for a user.
    
    Args:
        user_id: ID of the user who owns the task
        task_id: ID of the task to delete
        current_user: Currently authenticated user (from JWT)
        db: Database session dependency
    
    Returns:
        Success message confirming deletion
    
    Raises:
        HTTPException: If user_id in path doesn't match authenticated user or task not found
    """
    # Verify that the user_id in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )
    
    TaskService.delete_task(user_id, task_id, db)
    return {"message": "Task deleted successfully"}