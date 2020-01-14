from pydantic import BaseModel

class NoteSchema(BaseModel):
    title: str
    description: str 


class NoteDB(NoteSchema):
    id: int 


