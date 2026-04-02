from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.database import get_supabase
from app.schemas.profile import ScrapbookCreate

router = APIRouter(prefix="/scrapbook", tags=["scrapbook"])

@router.post("")
async def add_scrap(body: ScrapbookCreate, user_id: str, db=Depends(get_supabase)):
    exists = db.table("scrapbook") \
        .select("id") \
        .eq("user_id", user_id) \
        .eq("target_id", body.target_user_id) \
        .execute()
    if exists.data:
        raise HTTPException(status_code=409, detail="이미 스크랩됨")

    result = db.table("scrapbook").insert({
        "user_id": user_id,
        "target_id": body.target_user_id
    }).execute()
    return result.data[0]

@router.delete("/{target_user_id}")
async def remove_scrap(target_user_id: str, user_id: str, db=Depends(get_supabase)):
    db.table("scrapbook") \
        .delete() \
        .eq("user_id", user_id) \
        .eq("target_id", target_user_id) \
        .execute()
    return {"detail": "삭제 완료"}