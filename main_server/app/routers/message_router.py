from uuid import UUID
from fastapi import APIRouter, Depends
from supabase import Client
from app.dependencies.database import get_supabase
from app.dependencies.auth import get_current_user
import app.services.message_service as message_service

router = APIRouter(prefix="/messages", tags=["Message"])


@router.get("/{connection_id}")
async def read_messages(
    connection_id: UUID,
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase),
):
    return await message_service.read_messages(connection_id=str(connection_id), user=user, supabase=supabase)
