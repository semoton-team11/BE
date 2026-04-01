from fastapi import APIRouter, Depends, HTTPException
from database import get_supabase
from models import ProfileUpdate

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/{user_id}")
async def get_profile(user_id: str, db=Depends(get_supabase)):
    result = db.table("users").select("*").eq("id", user_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="유저 없음")
    return result.data


@router.patch("/{user_id}")
async def update_profile(user_id: str, body: ProfileUpdate, db=Depends(get_supabase)):
    updates = body.model_dump(exclude_none=True)
    
    check = db.table("users").select("*").eq("id", user_id).execute()
    if not check.data:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없어요!")
    
    if not updates:
        return check.data[0]  
    
    result = db.table("users").update(updates).eq("id", user_id).execute()
    return result.data[0]
