from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class NoteBase(BaseModel):
    """Base model for note creation and updates"""
    title: str = Field(..., min_length=3, max_length=255, description="Note title")
    description: str = Field(..., min_length=3, max_length=1000, description="Note description")
    completed: bool = Field(default=False, description="Completion status")


class NoteSchema(NoteBase):
    """Schema for creating/updating notes"""
    pass


class NoteDB(NoteBase):
    """Database model for notes with metadata"""
    id: int = Field(..., description="Unique note identifier")
    created_date: datetime = Field(..., description="Note creation timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Sample Note",
                "description": "This is a sample note",
                "completed": False,
                "created_date": "2024-01-15T10:30:00"
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response schema"""
    detail: str = Field(..., description="Error message")
