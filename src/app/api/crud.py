from app.api.models import NoteSchema, UserCreate
from app.db import notes, users
from sqlalchemy import select, insert, update, or_, and_
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Dict, Any


# --- User CRUD ---


async def create_user(
    session: AsyncSession, payload: UserCreate, hashed_password: str
) -> int:
    """Create a new user and return its ID"""
    query = (
        insert(users)
        .values(
            username=payload.username,
            email=payload.email,
            hashed_password=hashed_password,
            is_active=True,
        )
        .returning(users.c.id)
    )
    result = await session.execute(query)
    await session.commit()
    return result.scalar()


async def get_user_by_username(
    session: AsyncSession, username: str
) -> Optional[Dict[str, Any]]:
    """Retrieve a user by username"""
    query = select(users).where(users.c.username == username)
    result = await session.execute(query)
    row = result.mappings().first()
    return dict(row) if row else None


async def get_user_by_email(
    session: AsyncSession, email: str
) -> Optional[Dict[str, Any]]:
    """Retrieve a user by email"""
    query = select(users).where(users.c.email == email)
    result = await session.execute(query)
    row = result.mappings().first()
    return dict(row) if row else None


# --- Note CRUD ---


async def post(session: AsyncSession, payload: NoteSchema, owner_id: int) -> int:
    """Create a new note and return its ID"""
    query = (
        insert(notes)
        .values(
            title=payload.title,
            description=payload.description,
            completed=payload.completed,
            tags=payload.tags,
            owner_id=owner_id,
            is_deleted=False,
        )
        .returning(notes.c.id)
    )
    result = await session.execute(query)
    await session.commit()
    return result.scalar()


async def get(session: AsyncSession, id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a single note by ID"""
    query = select(notes).where(and_(notes.c.id == id, notes.c.is_deleted.is_(False)))
    result = await session.execute(query)
    row = result.mappings().first()
    return dict(row) if row else None


async def get_notes(
    session: AsyncSession,
    owner_id: int,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    completed: Optional[bool] = None,
    tag: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Retrieve notes for a specific owner with optional filtering and pagination"""
    # Enforce maximum limit to prevent abuse
    limit = min(limit, 100)

    query = select(notes).where(
        and_(notes.c.owner_id == owner_id, notes.c.is_deleted.is_(False))
    )

    # Apply filters
    filters = []

    if completed is not None:
        filters.append(notes.c.completed == completed)

    if tag:
        # Since we switched to JSON, we use a simple check
        search_tag = f'%"{tag}"%'
        filters.append(sa.cast(notes.c.tags, sa.String).ilike(search_tag))

    if search:
        search_pattern = f"%{search}%"
        filters.append(
            or_(
                notes.c.title.ilike(search_pattern),
                notes.c.description.ilike(search_pattern),
            )
        )

    # Combine filters with AND operator
    if filters:
        query = query.where(and_(*filters))

    # Apply pagination and ordering
    query = query.order_by(notes.c.created_date.desc()).offset(skip).limit(limit)

    result = await session.execute(query)
    return [dict(row) for row in result.mappings().all()]


async def put(session: AsyncSession, id: int, payload: NoteSchema) -> Optional[int]:
    """Update a note and return its ID if successful"""
    query = (
        update(notes)
        .where(and_(notes.c.id == id, notes.c.is_deleted.is_(False)))
        .values(
            title=payload.title,
            description=payload.description,
            completed=payload.completed,
            tags=payload.tags,
        )
        .returning(notes.c.id)
    )
    result = await session.execute(query)
    await session.commit()
    return result.scalar()


async def delete_note(session: AsyncSession, id: int) -> int:
    """Soft delete a note and return the number of rows affected"""
    query = update(notes).where(and_(notes.c.id == id, notes.c.is_deleted.is_(False))).values(is_deleted=True)
    result = await session.execute(query)
    await session.commit()
    return result.rowcount


async def delete_all(session: AsyncSession, owner_id: int) -> int:
    """Soft delete all notes for a specific owner and return the count"""
    query = update(notes).where(notes.c.owner_id == owner_id).values(is_deleted=True)
    result = await session.execute(query)
    await session.commit()
    return result.rowcount
