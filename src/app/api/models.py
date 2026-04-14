from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserDB(UserBase):
    id: int
    is_active: bool = True
    created_date: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class NoteBase(BaseModel):
    """Base model for note creation and updates"""

    title: str = Field(..., min_length=3, max_length=255, description="Note title")
    description: str = Field(
        ..., min_length=3, max_length=1000, description="Note description"
    )
    completed: bool = Field(default=False, description="Completion status")
    tags: List[str] = Field(default_factory=list, description="List of note tags")


class NoteSchema(NoteBase):
    """Schema for creating/updating notes"""

    pass


class NoteDB(NoteBase):
    """Database model for notes with metadata"""

    id: int = Field(..., description="Unique note identifier")
    created_date: datetime = Field(..., description="Note creation timestamp")
    is_deleted: bool = Field(default=False, description="Soft delete flag")
    owner_id: int = Field(..., description="ID of the user who owns this note")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Sample Note",
                "description": "This is a sample note",
                "completed": False,
                "tags": ["work", "important"],
                "is_deleted": False,
                "owner_id": 1,
                "created_date": "2024-01-15T10:30:00",
            }
        }
    )


class ErrorResponse(BaseModel):
    """Standard error response schema"""

    detail: str = Field(..., description="Error message")
