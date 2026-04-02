from uuid import UUID
from fastapi import APIRouter, Depends
from supabase import Client
from app.dependencies.database import get_supabase
from app.dependencies.auth import get_current_user
import app.services.message_service as message_service
from app.schemas.message import MessageCreate

router = APIRouter(prefix="/messages", tags=["Message"])


@router.get("/{connection_id}")
async def read_messages(
    connection_id: UUID,
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase),
):
    return await message_service.read_messages(connection_id=str(connection_id), user=user, supabase=supabase)

@router.post("/{connection_id}", status_code=201)
async def create_message(
    connection_id: UUID,
    body: MessageCreate,
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase),
):
    return await message_service.create_message(connection_id=str(connection_id), body=body, user=user, supabase=supabase)
