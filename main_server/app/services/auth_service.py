# app/services/auth_service.py

from app.schemas.auth import UserSignup, UserLogin
from datetime import datetime

class AuthService:
    @staticmethod
    def signup(user: UserSignup, supabase) -> dict:
        if user.is_graduated:
            calculated_grade = None
        else:
            current_year = datetime.now().year
            try:
                admission_year = int(user.student_id[:4])
                calculated_grade = current_year - admission_year + 1
            except ValueError:
                calculated_grade = None

        auth_response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "name": user.name,
                    "department": user.department,
                    "student_id": user.student_id,
                    "is_graduated": user.is_graduated,
                }
            },
        })

        if not auth_response.user:
            raise ValueError("Fail to Signup")

        user_id = auth_response.user.id

        user_data = {
            "id": user_id,
            "email": user.email,
            "name": user.name,
            "department": user.department,
            "student_id": user.student_id,
            "is_graduated": user.is_graduated,
            "grade": calculated_grade,
        }
        supabase.table("users").insert(user_data).execute()

        if user.is_graduated:
            senior_data = {
                "user_id": user_id,
                "bio": "아직 자기소개가 작성되지 않았습니다.",  # 디폴트 자기소개
                "job_title": "직무 미설정",                 # 디폴트 직함
                "company": "회사 미설정",                   # 디폴트 회사명
                "graduated_year": None,                     # 당장 알 수 없으므로 null 처리
                "is_available": True                        # 기본적으로 연결 가능 상태로 설정
            }
            supabase.table("senior_profiles").insert(senior_data).execute()

        return {"user_id": user_id}

    @staticmethod
    def login(user: UserLogin, supabase) -> dict:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password,
        })

        user_info = supabase.table("users").select("name").eq("id", response.user.id).single().execute()
        user_name = user_info.data.get("name") if user_info.data else "사용자"

        return {
            "access_token": response.session.access_token,
            "user_id": response.user.id,
            "name": user_name,
        }