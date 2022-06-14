from typing import List

from fastapi import APIRouter, Depends

from .. import schemas, service
from ...auth.permissions import get_user
from ...user import models

note_router = APIRouter()


@note_router.get('/note', response_model=List[schemas.GetNote])
async def list_notes():
    """ List notes router
    """
    return await service.note_s.all()


@note_router.post('/note', response_model=schemas.GetNote)
async def create_note(
        schema: schemas.CreateNote, user: models.User = Depends(get_user)
):
    """ Create note router
    """
    return await service.note_s.create(schema, user_id=user.id)
