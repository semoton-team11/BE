from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.dependencies.database import get_supabase

# security 객체 생성 (Swagger UI에 자물쇠 버튼을 생성)
security = HTTPBearer()

async def get_current_user(
    # Depends(security)를 통해 헤더에서 토큰을 자동으로 추출
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    HTTPBearer를 사용하면:
    - Swagger UI 우측 상단에 'Authorize' 버튼이 생김
    - 'Bearer '를 제외한 순수 토큰 문자열이 credentials.credentials에 담김
    """
    token = credentials.credentials
    
    try:
        supabase = get_supabase()
        
        # Supabase Auth에 토큰 검증 요청
        user_response = supabase.auth.get_user(token)
        
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid User.")
            
        # 유저의 UUID를 반환 (필요에 따라 user 객체 전체를 반환해도 됨)
        user = user_response.user
        return {
            "id": user.id,
            "email": user.email,
            "user_metadata": user.user_metadata,
        }
        
    except Exception:
        # 토큰이 만료되었거나 변조된 경우 여기로.
        raise HTTPException(status_code=401, detail="Fail to Auth.")