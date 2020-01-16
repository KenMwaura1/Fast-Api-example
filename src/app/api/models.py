from pydantic import BaseModel, Field

class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50) #additional validation for the inputs 
    description: str = Field(...,min_length=3, max_length=50)


class NoteDB(NoteSchema):
    id: int 


