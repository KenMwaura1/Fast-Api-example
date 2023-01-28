
from pydantic import BaseModel, Field, NonNegativeInt
from datetime import datetime as dt

class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50) #additional validation for the inputs 
    description: str = Field(...,min_length=3, max_length=50)
    completed: str = Field(...,min_length=3, max_length=8) 


class NoteDB(NoteSchema):
    id: int 
    created_date: str

