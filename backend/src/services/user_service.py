from sqlmodel import Session, select
from typing import Optional
from ..models.user import User, UserCreate, UserLogin
from fastapi import HTTPException, status
from passlib.context import CryptContext
from ..api.middleware.jwt_auth import create_access_token
from datetime import datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Service layer for user-related operations."""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.

        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password to compare against

        Returns:
            True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Generate a hash for a plain password.

        Args:
            password: Plain text password to hash

        Returns:
            Hashed password string
        """
        return pwd_context.hash(password)

    @classmethod
    def create_user(cls, user_create: UserCreate, db_session: Session) -> User:
        """
        Create a new user with hashed password.

        Args:
            user_create: User creation request with email and password
            db_session: Database session for the operation

        Returns:
            Created User object

        Raises:
            HTTPException: If email already exists
        """
        # Check if user already exists
        existing_user = db_session.exec(select(User).where(User.email == user_create.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user with hashed password
        hashed_password = cls.get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            password_hash=hashed_password
        )
        
        db_session.add(db_user)
        db_session.commit()
        db_session.refresh(db_user)
        
        return db_user

    @classmethod
    def authenticate_user(cls, email: str, password: str, db_session: Session) -> Optional[User]:
        """
        Authenticate a user with email and password.

        Args:
            email: User's email address
            password: User's plain text password
            db_session: Database session for the operation

        Returns:
            User object if authentication succeeds, None otherwise
        """
        user = db_session.exec(select(User).where(User.email == email)).first()
        if not user or not cls.verify_password(password, user.password_hash):
            return None
        return user

    @classmethod
    def login_user(cls, user_login: UserLogin, db_session: Session) -> tuple[User, str]:
        """
        Authenticate user and return user object with JWT token.

        Args:
            user_login: User login request with email and password
            db_session: Database session for the operation

        Returns:
            Tuple of (User object, JWT access token)

        Raises:
            HTTPException: If authentication fails
        """
        user = cls.authenticate_user(user_login.email, user_login.password, db_session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create JWT token with user data
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
        access_token = create_access_token(data=token_data)
        
        return user, access_token