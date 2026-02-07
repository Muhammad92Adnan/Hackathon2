from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TaskBase(SQLModel):
    """Base model for task with common fields."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default="", max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """Todo task item owned by a user."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: "User" = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    title: str
    description: Optional[str] = None


class TaskRead(TaskBase):
    """Schema for returning task data."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskToggle(BaseModel):
    """Schema for toggling task completion."""
    completed: bool