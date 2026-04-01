from fastapi import APIRouter, Depends
from database import get_supabase

router = APIRouter(prefix="/connections", tags=["connections"])

@router.get("")
async def get_connections(user_id: str, db=Depends(get_supabase)):
    result = db.table("connections") \
        .select("*, senior:users!senior_id(id, name, major, avatar_url)") \
        .eq("junior_id", user_id) \
        .order("created_at", desc=True) \
        .execute()
    return result.data