from datetime import date
from fastapi import HTTPException
from postgrest.exceptions import APIError
from app.schemas.schedule import ScheduleCreate
from app.utils.responses import success_response

SCHEDULE_COLUMNS = "id, mentor_id, mentee_id, available_date, start_time, end_time, is_reserved, created_at"


async def create_schedule(body: ScheduleCreate, user: dict, supabase):
    # connection 존재 여부 및 accepted 상태 확인
    try:
        connection = (
            supabase.table("connections")
            .select("id, requester_id, senior_id, status")
            .eq("id", str(body.connection_id))
            .maybe_single()
            .execute()
        )
    except APIError:
        raise HTTPException(status_code=500, detail={"message": "연결 조회에 실패했습니다.", "code": "FETCH_FAILED"})

    if not connection.data:
        raise HTTPException(status_code=404, detail={"message": "연결을 찾을 수 없습니다.", "code": "CONNECTION_NOT_FOUND"})

    if connection.data["status"] != "accepted":
        raise HTTPException(status_code=403, detail={"message": "수락된 연결에서만 약속을 잡을 수 있습니다.", "code": "CONNECTION_NOT_ACCEPTED"})

    requester_id = connection.data["requester_id"]
    senior_id = connection.data["senior_id"]

    # senior_id는 senior_profiles.id이므로 user_id로 변환
    senior_profile = (
        supabase.table("senior_profiles")
        .select("user_id")
        .eq("id", senior_id)
        .maybe_single()
        .execute()
    )
    if not senior_profile.data:
        raise HTTPException(status_code=500, detail={"message": "선배 프로필을 찾을 수 없습니다.", "code": "SENIOR_NOT_FOUND"})

    senior_user_id = senior_profile.data["user_id"]

    if user["id"] not in [requester_id, senior_user_id]:
        raise HTTPException(status_code=403, detail={"message": "권한이 없습니다.", "code": "FORBIDDEN"})

    # 더블 부킹 검증
    overlap = (
        supabase.table("mentoring_slots")
        .select("id")
        .eq("mentor_id", senior_user_id)
        .eq("available_date", body.available_date.isoformat())
        .eq("is_reserved", True)
        .lt("start_time", body.end_time.isoformat())
        .gt("end_time", body.start_time.isoformat())
        .execute()
    )
    if overlap.data:
        raise HTTPException(status_code=409, detail={"message": "해당 시간에 이미 약속이 있습니다.", "code": "TIME_CONFLICT"})

    try:
        response = (
            supabase.table("mentoring_slots")
            .insert({
                "mentor_id": senior_user_id,
                "mentee_id": requester_id,
                "available_date": body.available_date.isoformat(),
                "start_time": body.start_time.isoformat(),
                "end_time": body.end_time.isoformat(),
                "is_reserved": True,
            })
            .execute()
        )
    except APIError:
        raise HTTPException(status_code=500, detail={"message": "약속 생성에 실패했습니다.", "code": "CREATE_FAILED"})

    return success_response(data=response.data[0], message="약속이 생성됐습니다.")


async def read_schedules(user: dict, supabase):
    try:
        schedules = (
            supabase.table("mentoring_slots")
            .select(SCHEDULE_COLUMNS)
            .eq("is_reserved", True)
            .or_(f'mentor_id.eq.{user["id"]},mentee_id.eq.{user["id"]}')
            .gte("available_date", date.today().isoformat())
            .order("available_date", desc=False)
            .order("start_time", desc=False)
            .execute()
        )
    except APIError:
        raise HTTPException(status_code=500, detail={"message": "약속 목록 조회에 실패했습니다.", "code": "FETCH_FAILED"})

    return success_response(data=schedules.data)
