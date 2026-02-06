from pydantic import BaseModel, EmailStr, Field, field_validator


# Request Models
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)
    confirm_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserUpdate(BaseModel):
    address: str | None = Field(None, min_length=5, max_length=255)
    gender: str | None = None
    age: int | None = Field(None, ge=1, le=120)

    @field_validator('address')
    def validate_address(cls, v):
        if v is not None and v.strip():
            if len(v.strip()) < 5:
                raise ValueError('Address must be at least 5 characters long')
            if not any(c.isalnum() for c in v):
                raise ValueError('Address must contain one letter or number')
        return v.strip() if v else None


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=6)


class TokenData(BaseModel):
    email: str | None = None


# Response Models
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    address: str | None = None
    gender: str | None = None
    age: int | None = None
    
    class Config:
        from_attributes = True  # Allows creating from SQLAlchemy models


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class MessageResponse(BaseModel):
    message: str
    success: bool = True


class ProfileUpdateResponse(BaseModel):
    message: str
    success: bool
    user: UserResponse
