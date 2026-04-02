from uuid import UUID
from fastapi import APIRouter, Depends, Query
from supabase import Client
from typing import Optional
from app.dependencies.database import get_supabase
import app.services.senior_service as senior_service

router = APIRouter(prefix="/seniors", tags=["Senior"])


@router.get("")
async def list_seniors(
    department: Optional[str] = Query(None, description="학과 필터 (예: 산업디자인학과)"),
    supabase: Client = Depends(get_supabase),
):
    return await senior_service.list_seniors(department=department, supabase=supabase)


@router.get("/{senior_id}")
async def get_senior(
    senior_id: UUID,
    supabase: Client = Depends(get_supabase),
):
    return await senior_service.get_senior(senior_id=str(senior_id), supabase=supabase)
