"""
Authentication endpoints - Signup and Login
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User, UserCreate, UserLogin, UserResponse
from app.auth import hash_password, verify_password, create_access_token
import uuid

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=dict, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Create a new user account

    - Validates email is unique
    - Hashes password with bcrypt
    - Creates user in database
    - Returns JWT token and user info
    """
    # Check if email already exists
    statement = select(User).where(User.email == user_data.email.lower())
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Determine user role (admin for specific email)
    ADMIN_EMAIL = "asif.alimusharaf@gmail.com"
    user_role = "admin" if user_data.email.lower() == ADMIN_EMAIL else "user"

    # Create new user
    user = User(
        id=str(uuid.uuid4()),
        email=user_data.email.lower(),
        name=user_data.name,
        hashed_password=hash_password(user_data.password),
        role=user_role
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Generate JWT token
    token = create_access_token(data={"sub": user.id, "email": user.email})

    # Return response
    user_response = UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        created_at=user.created_at
    )

    return {
        "token": token,
        "user": user_response.model_dump(mode='json')
    }


@router.post("/login", response_model=dict)
def login(credentials: UserLogin, session: Session = Depends(get_session)):
    """
    Authenticate existing user

    - Verifies email exists
    - Verifies password hash
    - Returns JWT token and user info
    """
    # Find user by email
    statement = select(User).where(User.email == credentials.email.lower())
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    token = create_access_token(data={"sub": user.id, "email": user.email})

    # Return response
    user_response = UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        created_at=user.created_at
    )

    return {
        "token": token,
        "user": user_response.model_dump(mode='json')
    }
