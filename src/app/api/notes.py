from app.api import crud
from app.api.models import NoteDB, NoteSchema, ErrorResponse, UserDB
from app.api.dependencies import get_current_active_user
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Path, Query, Depends
from typing import List, Optional

router = APIRouter()


@router.post(
    "/",
    response_model=NoteDB,
    status_code=201,
    responses={400: {"model": ErrorResponse}},
)
async def create_note(
    payload: NoteSchema,
    session: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_active_user),
):
    """Create a new note"""
    try:
        note_id = await crud.post(session, payload, owner_id=current_user.id)
        response = await crud.get(session, note_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create note: {str(e)}")


@router.get("/", response_model=List[NoteDB], responses={400: {"model": ErrorResponse}})
async def read_notes(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of items to return"
    ),
    search: Optional[str] = Query(
        None, max_length=100, description="Search term for title/description"
    ),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    session: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_active_user),
):
    """
    Retrieve notes with optional filtering and pagination.

    - **skip**: Number of items to skip (default: 0)
    - **limit**: Maximum items per page (default: 10, max: 100)
    - **search**: Search in title and description fields
    - **completed**: Filter by completion status (true/false)
    - **tag**: Filter notes that contain this specific tag
    """
    try:
        return await crud.get_notes(
            session,
            owner_id=current_user.id,
            skip=skip,
            limit=limit,
            search=search,
            completed=completed,
            tag=tag,
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to retrieve notes: {str(e)}"
        )


@router.get(
    "/{id}",
    response_model=NoteDB,
    responses={404: {"model": ErrorResponse}, 422: {"description": "Invalid note ID"}},
)
async def read_note(
    id: int = Path(..., gt=0, description="Note ID"),
    session: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_active_user),
):
    """Retrieve a specific note by ID"""
    try:
        note = await crud.get(session, id)
        if not note or note["owner_id"] != current_user.id:
            raise HTTPException(status_code=404, detail=f"Note with id {id} not found")
        return note
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to retrieve note: {str(e)}"
        )


@router.put(
    "/{id}",
    response_model=NoteDB,
    responses={404: {"model": ErrorResponse}, 422: {"description": "Invalid note ID"}},
)
async def update_note(
    id: int = Path(..., gt=0, description="Note ID"),
    payload: NoteSchema = None,
    session: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_active_user),
):
    """Update an existing note"""
    try:
        note = await crud.get(session, id)
        if not note or note["owner_id"] != current_user.id:
            raise HTTPException(status_code=404, detail=f"Note with id {id} not found")
        await crud.put(session, id, payload)
        response = await crud.get(session, id)
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update note: {str(e)}")


@router.delete(
    "/{id}",
    response_model=NoteDB,
    responses={404: {"model": ErrorResponse}, 422: {"description": "Invalid note ID"}},
)
async def delete_note(
    id: int = Path(..., gt=0, description="Note ID"),
    session: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_active_user),
):
    """Delete a note by ID"""
    try:
        note = await crud.get(session, id)
        if not note or note["owner_id"] != current_user.id:
            raise HTTPException(status_code=404, detail=f"Note with id {id} not found")
        await crud.delete_note(session, id)
        return note
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete note: {str(e)}")
