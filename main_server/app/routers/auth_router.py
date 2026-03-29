from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.auth import UserSignup, UserLogin
from app.dependencies.database import get_supabase

router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase=Depends(get_supabase),
):
    token = credentials.credentials
    try:
        response = supabase.auth.get_user(token)
        if not response.user:
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
        return response.user
    except Exception:
        raise HTTPException(status_code=401, detail="인증에 실패했습니다.")


@router.post("/signup")
async def signup(user: UserSignup, supabase=Depends(get_supabase)):
    try:
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "department": user.department,
                    "student_id": user.student_id,
                }
            },
        })
        return {"message": "회원가입 성공!", "user": response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(user: UserLogin, supabase=Depends(get_supabase)):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password,
        })
        return {
            "message": "로그인 성공!",
            "access_token": response.session.access_token,
            "user_id": response.user.id,
        }
    except Exception:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 잘못되었습니다.")


@router.get("/me")
async def get_me(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "user_metadata": user.user_metadata,
        "last_sign_in_at": user.last_sign_in_at,
    }
