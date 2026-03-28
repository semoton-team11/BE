from fastapi import APIRouter, HTTPException, Depends
from server.models.schemas import UserAuth, UserLogin
from server.core.config import supabase
from server.core.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

# 회원가입
@router.post("/signup")
async def signup(user: UserAuth):
    try:
        # Supabase Auth를 이용해 유저 생성
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "department": user.department,
                    "student_id": user.student_id
                }
            }
        })
        return {"message": "회원가입 성공!", "user": response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# 로그인
@router.post("/login")
async def login(user: UserLogin):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password,
        })
        # 로그인 성공 시 세션 토큰 반환
        return {
            "message": "로그인 성공!",
            "access_token": response.session.access_token,
            "user_id": response.user.id
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 잘못되었습니다.")
    
# 로그인 성공시 보이는 화면
@router.get("/me")
async def get_me(user = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "user_metadata": user.user_metadata,
        "last_sign_in_at": user.last_sign_in_at
    }