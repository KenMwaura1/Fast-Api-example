from app.api.models import NoteSchema
from app.db import notes, database
from sqlalchemy import or_, and_
from typing import Optional, List, Dict, Any


async def post(payload: NoteSchema) -> int:
    """Create a new note and return its ID"""
    query = notes.insert().values(
        title=payload.title,
        description=payload.description,
        completed=payload.completed
    )
    return await database.execute(query=query)


async def get(id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a single note by ID"""
    query = notes.select().where(notes.c.id == id)
    return await database.fetch_one(query=query)


async def get_notes(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    completed: Optional[bool] = None
) -> List[Dict[str, Any]]:
    """Retrieve notes with optional filtering and pagination"""
    # Enforce maximum limit to prevent abuse
    limit = min(limit, 100)
    
    query = notes.select()
    
    # Apply filters
    filters = []
    if completed is not None:
        filters.append(notes.c.completed == completed)
        
    if search:
        search_pattern = f"%{search}%"
        filters.append(
            or_(
                notes.c.title.ilike(search_pattern),
                notes.c.description.ilike(search_pattern)
            )
        )
    
    # Combine filters with AND operator
    if filters:
        query = query.where(and_(*filters))
    
    # Apply pagination and ordering
    query = query.order_by(notes.c.created_date.desc()).offset(skip).limit(limit)
    
    return await database.fetch_all(query=query)


async def put(id: int, payload: NoteSchema) -> Optional[int]:
    """Update a note and return its ID if successful"""
    query = (
        notes.update()
        .where(notes.c.id == id)
        .values(
            title=payload.title,
            description=payload.description,
            completed=payload.completed
        )
        .returning(notes.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int) -> int:
    """Delete a note and return the number of rows deleted"""
    query = notes.delete().where(notes.c.id == id)
    return await database.execute(query=query)


async def delete_all() -> int:
    """Delete all notes (use with caution) and return the count"""
    query = notes.delete()
    return await database.execute(query=query)
