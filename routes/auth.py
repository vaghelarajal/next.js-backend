from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config import get_db, Base, engine
from utils import hash_password, verify_password, create_access_token, verify_token, get_current_user
from models import User
from schemas import (
    UserCreate, UserLogin, UserUpdate,
    ForgotPasswordRequest, ResetPasswordRequest,
    LoginResponse, MessageResponse, ProfileUpdateResponse, UserResponse
)
from services import send_reset_email, is_token_used, mark_token_as_used
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY_CHANGE_THIS")
ALGORITHM = "HS256"
RESET_TOKEN_EXPIRE_MINUTES = 10
FRONTEND_RESET_URL = os.getenv("FRONTEND_RESET_URL")

# Create tables on first import
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error creating tables: {e}")

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED,
             response_model=MessageResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Validate password confirmation
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Check email exist
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user with hashed pwd
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    # Save to db
    db.add(new_user)
    db.commit()
    return MessageResponse(message="User registered successfully",
                           success=True)


@router.post("/login", response_model=LoginResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Find user by email
    db_user = db.query(User).filter(User.email == user.email).first()
    # Verifications
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create jwt token
    return LoginResponse(
        access_token=create_access_token({"sub": db_user.email}),
        token_type="bearer",
        user=UserResponse.model_validate(db_user)
    )


@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(
    data: ForgotPasswordRequest, db: Session = Depends(get_db)
):
    """Send password reset email to user"""
    try:
        # Find user by email
        user = db.query(User).filter(User.email == data.email).first()
        if not user:
            return MessageResponse(
                message="Password reset link has been sent.",
                success=True
            )

        # Generate reset token
        token = create_access_token(
            {"sub": user.email, "type": "password_reset"},
            expires_delta=timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
        )
        reset_link = f"{FRONTEND_RESET_URL}?token={token}"

        # Attempt to send email
        try:
            send_reset_email(user.email, reset_link)
            return MessageResponse(
                message="Password reset link has been sent, please check.",
                success=True
            )
        except Exception:
            # Still return success to not reveal if email exists
            return MessageResponse(
                message="Password reset link has been sent.",
                success=True
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process password reset request"
        )


@router.post("/reset-password", response_model=MessageResponse)
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset user password using token"""
    try:
        # Check if token has been used
        if is_token_used(data.token, db):
            raise HTTPException(status_code=400,
                                detail="Reset link has already been used")
        # Decode and validate token
        payload = jwt.decode(data.token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        token_type = payload.get("type")
        if not email or token_type != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset token"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )

    try:
        # Find user and update password
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if new password is different from current password
        if verify_password(data.new_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different from your old password"
            )

        # Mark token as used BEFORE updating password
        mark_token_as_used(data.token, user.email, db)
        # Update password
        user.password = hash_password(data.new_password)
        db.commit()

        return MessageResponse(
            message="Password reset successful.",
            success=True
        )
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password"
        )


@router.put("/profile", response_model=ProfileUpdateResponse)
@router.patch("/profile", response_model=ProfileUpdateResponse)
def update_profile(
    user_data: UserUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile information - requires JWT authentication"""
    try:
        # Update only provided fields
        updated_fields = []
        if user_data.address is not None:
            user.address = user_data.address
            updated_fields.append("address")
        if user_data.gender is not None:
            user.gender = user_data.gender
            updated_fields.append("gender")
        if user_data.age is not None:
            user.age = user_data.age
            updated_fields.append("age")
        if not updated_fields:
            return ProfileUpdateResponse(
                message="No changes made to profile",
                success=True,
                user=UserResponse.model_validate(user)
            )

        # Commit changes
        db.commit()
        db.refresh(user)

        return ProfileUpdateResponse(
            message=f"Updated successfully: {', '.join(updated_fields)}",
            success=True,
            user=UserResponse.model_validate(user)
        )
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    user: User = Depends(get_current_user)
):
    """Get current user information - requires JWT authentication"""
    return UserResponse.model_validate(user)
