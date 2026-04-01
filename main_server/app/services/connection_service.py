from fastapi import HTTPException
from postgrest.exceptions import APIError
from app.schemas.connection import ConnectionCreate
from app.utils.responses import success_response

CONNECTIONS_COLUMNS = "id, requester_id, senior_id, status, message, created_at"


async def create_connection(body: ConnectionCreate, user: dict, supabase):
    # 선배 프로필 존재 여부, 가용성, 자기 자신 여부 검증
    try:
        senior = (
            supabase.table("senior_profiles")
            .select("id, user_id, is_available")
            .eq("id", str(body.senior_id))
            .maybe_single()
            .execute()
        )
    except APIError:
        raise HTTPException(status_code=400, detail={"message": "잘못된 senior_id 입니다.", "code": "INVALID_SENIOR_ID"})

    if not senior.data:
        raise HTTPException(status_code=404, detail={"message": "선배 프로필을 찾을 수 없습니다.", "code": "SENIOR_NOT_FOUND"})
    if senior.data["user_id"] == user["id"]:
        raise HTTPException(status_code=400, detail={"message": "본인에게는 연결 요청을 보낼 수 없습니다.", "code": "SELF_CONNECTION"})
    if not senior.data["is_available"]:
        raise HTTPException(status_code=400, detail={"message": "현재 연결 요청을 받을 수 없는 선배입니다.", "code": "SENIOR_UNAVAILABLE"})

    # DB unique index가 중복을 보장 → insert 실패 시 409 반환
    try:
        response = (
            supabase.table("connections")
            .insert({
                "requester_id": user["id"],
                "senior_id": str(body.senior_id),
                "status": "pending",
                "message": body.message,
            })
            .execute()
        )
    except APIError as e:
        if "duplicate" in str(e).lower() or "unique" in str(e).lower():
            raise HTTPException(status_code=409, detail={"message": "이미 진행 중이거나 연결된 요청입니다.", "code": "DUPLICATE_CONNECTION"})
        raise

    return success_response(data=response.data[0], message="연결 요청을 보냈습니다.")


async def _update_connection_status(connection_id: str, new_status: str, user: dict, supabase):
    """accept/reject 공통 로직"""
    try:
        connection = (
            supabase.table("connections")
            .select(CONNECTIONS_COLUMNS)
            .eq("id", connection_id)
            .maybe_single()
            .execute()
        )
    except APIError:
        raise HTTPException(status_code=400, detail={"message": "잘못된 connection_id 입니다.", "code": "INVALID_CONNECTION_ID"})

    if not connection.data:
        raise HTTPException(status_code=404, detail={"message": "연결 요청을 찾을 수 없습니다.", "code": "CONNECTION_NOT_FOUND"})

    # 참여자 확인이 아닌 "선배 본인"만 수락/거절 가능하므로
    # get_connection_as_participant 대신 직접 조회
    senior_profile = (
        supabase.table("senior_profiles")
        .select("id")
        .eq("id", connection.data["senior_id"])
        .eq("user_id", user["id"])
        .execute()
    )
    if not senior_profile.data:
        raise HTTPException(status_code=403, detail={"message": "권한이 없습니다.", "code": "FORBIDDEN"})

    # pending 상태인 row만 업데이트 (경쟁 상황 방지)
    response = (
        supabase.table("connections")
        .update({"status": new_status})
        .eq("id", connection_id)
        .eq("status", "pending")
        .execute()
    )
    if not response.data:
        raise HTTPException(status_code=409, detail={"message": "이미 처리된 요청입니다.", "code": "ALREADY_PROCESSED"})

    return response.data[0]


async def accept_connection(connection_id: str, user: dict, supabase):
    data = await _update_connection_status(connection_id, "accepted", user, supabase)
    return success_response(data=data, message="연결 요청을 수락했습니다.")


async def reject_connection(connection_id: str, user: dict, supabase):
    data = await _update_connection_status(connection_id, "rejected", user, supabase)
    return success_response(data=data, message="연결 요청을 거절했습니다.")


async def read_connections(user: dict, supabase):
    sent = (
        supabase.table("connections")
        .select(CONNECTIONS_COLUMNS)
        .eq("requester_id", user["id"])
        .execute()
    )

    senior_profile = (
        supabase.table("senior_profiles")
        .select("id")
        .eq("user_id", user["id"])
        .execute()
    )
    received = []
    if senior_profile.data:
        senior_id = senior_profile.data[0]["id"]
        received_res = (
            supabase.table("connections")
            .select(CONNECTIONS_COLUMNS)
            .eq("senior_id", senior_id)
            .execute()
        )
        received = received_res.data

    return success_response(data={"sent": sent.data, "received": received})
