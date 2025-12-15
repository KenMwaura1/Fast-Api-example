from app.api import crud
from app.api.models import NoteDB, NoteSchema
from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Optional

router = APIRouter()


@router.post("/", response_model=NoteDB, status_code=201)
async def create_note(payload: NoteSchema):
    note_id = await crud.post(payload)
    response = await crud.get(note_id)
    return response


@router.get("/", response_model=List[NoteDB])
async def read_notes(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    completed: Optional[bool] = None
):
    return await crud.get_notes(skip=skip, limit=limit, search=search, completed=completed)


@router.get("/{id}/", response_model=NoteDB)
async def read_note(id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{id}/", response_model=NoteDB)
async def update_note(payload: NoteSchema, id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    await crud.put(id, payload)
    response = await crud.get(id)
    return response


@router.delete("/{id}/", response_model=NoteDB)
async def delete_note(id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    await crud.delete(id)
    return note


