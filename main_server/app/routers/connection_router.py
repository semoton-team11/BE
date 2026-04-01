from uuid import UUID
from fastapi import APIRouter, Depends
from supabase import Client
from app.schemas.connection import ConnectionCreate
from app.dependencies.database import get_supabase
from app.dependencies.auth import get_current_user
import app.services.connection_service as connection_service

router = APIRouter(prefix="/connections", tags=["Connection"])


@router.post("", status_code=201)
async def create_connection(
    body: ConnectionCreate,
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase),
):
    return await connection_service.create_connection(body=body, user=user, supabase=supabase)


@router.patch("/{connection_id}/accept")
async def accept_connection(
    connection_id: UUID,
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase),
):
    return await connection_service.accept_connection(connection_id=str(connection_id), user=user, supabase=supabase)


@router.patch("/{connection_id}/reject")
async def reject_connection(
    connection_id: UUID,
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase),
):
    return await connection_service.reject_connection(connection_id=str(connection_id), user=user, supabase=supabase)


@router.get("")
async def read_connections(
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase),
):
    return await connection_service.read_connections(user=user, supabase=supabase)
