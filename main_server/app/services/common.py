from fastapi import HTTPException
from postgrest.exceptions import APIError
from supabase import Client


async def get_connection_as_participant(connection_id: str, user: dict, supabase: Client):
    """connection 조회 + 참여자 검증을 한 번에 처리하는 공통 유틸"""
    try:
        connection = (
            supabase.table("connections")
            .select("id, requester_id, senior_id, status, senior_profiles(user_id)")
            .eq("id", connection_id)
            .maybe_single()
            .execute()
        )
    except APIError:
        raise HTTPException(status_code=500, detail={"message": "연결 조회에 실패했습니다.", "code": "FETCH_FAILED"})

    if not connection.data:
        raise HTTPException(status_code=404, detail={"message": "연결을 찾을 수 없습니다.", "code": "CONNECTION_NOT_FOUND"})

    conn = connection.data
    senior_profile = conn.get("senior_profiles")
    if not senior_profile:
        raise HTTPException(status_code=500, detail={"message": "연결된 선배 프로필이 존재하지 않습니다.", "code": "SENIOR_PROFILE_MISSING"})

    senior_user_id = senior_profile["user_id"]
    if conn["requester_id"] != user["id"] and senior_user_id != user["id"]:
        raise HTTPException(status_code=403, detail={"message": "권한이 없습니다.", "code": "FORBIDDEN"})

    return conn
