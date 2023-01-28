import datetime
from pydantic import BaseModel, Field


class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50) #additional validation for the inputs 
    description: str = Field(...,min_length=3, max_length=50)
    completed: str = Field(...,min_length=3, max_length=8) 
    created_date: datetime.datetime = Field(default_factory=datetime.datetime.now)


class NoteDB(NoteSchema):
    id: int 
    created_date: datetime.datetime


