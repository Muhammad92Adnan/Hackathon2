from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import bcrypt
from pydantic import BaseModel


class UserBase(SQLModel):
    """Base model for user with common fields."""
    email: str = Field(unique=True, index=True, max_length=255)


class User(UserBase, table=True):
    """User account with authentication credentials."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str

    def hash_password(self) -> str:
        """Hash the password before storing."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(self.password.encode('utf-8'), salt).decode('utf-8')


class UserRead(UserBase):
    """Schema for returning user data (without password)."""
    id: int
    created_at: datetime


class UserLogin(BaseModel):
    """Schema for user login."""
    email: str
    password: str