from app.api.models import NoteSchema
from app.db import notes, database
from sqlalchemy import or_


async def post(payload: NoteSchema):
    query = notes.insert().values(title=payload.title,
                                  description=payload.description, completed=payload.completed)
    return await database.execute(query=query)


async def get(id: int):
    query = notes.select().where(id == notes.c.id)
    return await database.fetch_one(query=query)


async def get_notes(skip: int = 0, limit: int = 10, search: str = None, completed: bool = None):
    query = notes.select()
    
    if completed is not None:
        query = query.where(notes.c.completed == completed)
        
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                notes.c.title.ilike(search_pattern),
                notes.c.description.ilike(search_pattern)
            )
        )
        
    query = query.offset(skip).limit(limit)
    return await database.fetch_all(query=query)


async def put(id: int, payload: NoteSchema):
    query = (
        notes.update().where(id == notes.c.id).values(title=payload.title,
                                                      description=payload.description, completed=payload.completed)
        .returning(notes.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = notes.delete().where(id == notes.c.id)
    return await database.execute(query=query)


async def delete_all():
    query = notes.delete()
    return await database.execute(query=query)
