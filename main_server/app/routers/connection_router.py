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

 # 목록 조회
@router.get("")
async def read_connections(
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase),
):
    return await connection_service.read_connections(user=user, supabase=supabase)

# 다애님 구현 : userId를 받아서 누구든지 조회가능
"""
@router.get("")
async def get_connections(user_id: str, db=Depends(get_supabase)):
    user: dict = Depends(get_current_user),
    result = db.table("connections") \
        .select("*, senior:users!senior_id(id, name, major, avatar_url)") \
        .eq("junior_id", user_id) \
        .order("created_at", desc=True) \
        .execute()
    return result.data
"""