from fastapi import APIRouter, HTTPException, Depends
from app.schemas.auth import UserSignup, UserLogin
from app.dependencies.database import get_supabase
from app.utils.responses import success_response
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def signup(user: UserSignup, supabase=Depends(get_supabase)):
    try:
        auth_response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "name": user.name,
                    "department": user.department,
                    "student_id": user.student_id,
                    "is_graduated": user.is_graduated
                }
            },
        })

        if not auth_response.user:
            raise Exception("Fail to Signup")

        user_data = {
            "id": auth_response.user.id,
            "email": user.email,
            "name": user.name,
            "department": user.department,
            "student_id": user.student_id,
            "is_graduated": user.is_graduated,
        }
        supabase.table("users").insert(user_data).execute()

        return success_response(
            data={"user_id": auth_response.user.id},
            message="Success to Signup"
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(user: UserLogin, supabase=Depends(get_supabase)):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password,
        })

        user_info = supabase.table("users").select("name").eq("id", response.user.id).single().execute()
        user_name = user_info.data.get("name") if user_info.data else "사용자"

        return success_response(data={
            "access_token": response.session.access_token,
            "user_id": response.user.id,
            "name": user_name,
        }, message="Success to Login")

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid email or password")


@router.get("/me")
async def get_me(user=Depends(get_current_user)):
    return success_response(data=user)
