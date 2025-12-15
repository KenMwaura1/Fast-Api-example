from pydantic import BaseModel, Field
from datetime import datetime


class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)
    completed: bool = False


class NoteDB(NoteSchema):
    id: int
    created_date: datetime
