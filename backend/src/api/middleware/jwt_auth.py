from fastapi import HTTPException, status, Request
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from ..config import settings
from typing import Dict, Optional
from datetime import datetime, timedelta
from ..models.user import UserRead


security = HTTPBearer()


def create_access_token(data: dict) -> str:
    """
    Create a JWT access token with expiration.

    Args:
        data: Dictionary containing data to encode in token (typically user info)

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Dict:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string to verify

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid, expired, or malformed
    """
    try:
        payload = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(request: Request) -> UserRead:
    """
    Get the current authenticated user from the request.

    Args:
        request: FastAPI request object containing the authorization header

    Returns:
        UserRead object representing the authenticated user

    Raises:
        HTTPException: If no valid token is provided or user doesn't exist
    """
    credentials: HTTPAuthorizationCredentials = await security(request)
    token = credentials.credentials
    
    payload = verify_token(token)
    user_id: int = payload.get("user_id")
    email: str = payload.get("email")
    
    if user_id is None or email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Return a UserRead object with the validated user data
    return UserRead(id=user_id, email=email, created_at=payload.get("created_at"))