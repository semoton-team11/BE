from fastapi import APIRouter, Depends
from supabase import Client
from app.schemas.schedule import ScheduleCreate
from app.dependencies.database import get_supabase
from app.dependencies.auth import get_current_user
import app.services.schedule_service as schedule_service

router = APIRouter(prefix="/schedules", tags=["Schedule"])


@router.post("", status_code=201)
async def create_schedule(
    body: ScheduleCreate,
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase),
):
    return await schedule_service.create_schedule(body=body, user=user, supabase=supabase)


@router.get("")
async def read_schedules(
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase),
):
    return await schedule_service.read_schedules(user=user, supabase=supabase)
