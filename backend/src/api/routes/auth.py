from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..db.database import get_session
from ..models.user import UserCreate, UserLogin, UserRead
from ..services.user_service import UserService
from pydantic import BaseModel


router = APIRouter()


@router.post("/signup", response_model=UserRead)
async def signup(user_create: UserCreate, db: Session = Depends(get_session)):
    """
    Register a new user with email and password.
    
    Args:
        user_create: User creation request with email and password
        db: Database session dependency
    
    Returns:
        Created user object (without password)
    
    Raises:
        HTTPException: If email already exists
    """
    try:
        db_user = UserService.create_user(user_create, db)
        return UserRead(
            id=db_user.id,
            email=db_user.email,
            created_at=db_user.created_at
        )
    except HTTPException:
        # Re-raise HTTP exceptions from the service layer
        raise
    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during registration: {str(e)}"
        )


@router.post("/signin")
async def signin(user_login: UserLogin, db: Session = Depends(get_session)):
    """
    Authenticate user with email and password, returning JWT token.
    
    Args:
        user_login: User login request with email and password
        db: Database session dependency
    
    Returns:
        Dictionary containing user info and access token
    
    Raises:
        HTTPException: If authentication fails
    """
    try:
        user, access_token = UserService.login_user(user_login, db)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserRead(
                id=user.id,
                email=user.email,
                created_at=user.created_at
            )
        }
    except HTTPException:
        # Re-raise HTTP exceptions from the service layer
        raise
    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}"
        )


@router.post("/signout")
async def signout():
    """
    Sign out the user (client-side operation).
    
    Returns:
        Success message confirming logout
    """
    # This is primarily a client-side operation where the JWT token is cleared
    # The backend doesn't maintain session state for JWT tokens
    return {"message": "Successfully signed out. Please clear your token on the client."}