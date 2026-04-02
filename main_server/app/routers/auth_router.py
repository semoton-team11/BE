# app/routers/auth.py

from fastapi import APIRouter, HTTPException, Depends
from app.schemas.auth import UserSignup, UserLogin
from app.dependencies.database import get_supabase
from app.utils.responses import success_response
from app.dependencies.auth import get_current_user
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
async def signup(user: UserSignup, supabase=Depends(get_supabase)):
    try:
        result = AuthService.signup(user, supabase)
        return success_response(
            data=result,
            message="Success to Signup"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(user: UserLogin, supabase=Depends(get_supabase)):
    try:
        result = AuthService.login(user, supabase)
        return success_response(
            data=result, 
            message="Success to Login"
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid email or password")


@router.get("/me")
async def get_me(user=Depends(get_current_user)):
    return success_response(data=user)