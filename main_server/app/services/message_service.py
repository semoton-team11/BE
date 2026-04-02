from fastapi import HTTPException
from app.utils.responses import success_response
from app.services.common import get_connection_as_participant
from postgrest.exceptions import APIError
from app.schemas.message import MessageCreate

MESSAGE_COLUMNS = "id, connection_id, sender_id, content, is_read, created_at"


async def read_messages(connection_id: str, user: dict, supabase):
    conn = await get_connection_as_participant(connection_id, user, supabase)

    # 수락된 연결에서만 메시지 조회 가능
    if conn["status"] != "accepted":
        raise HTTPException(status_code=403, detail={"message": "수락된 연결에서만 메시지를 조회할 수 있습니다.", "code": "CONNECTION_NOT_ACCEPTED"})

    try:
        messages = (
            supabase.table("messages")
            .select(MESSAGE_COLUMNS)
            .eq("connection_id", connection_id)
            .order("created_at", desc=False)
            .execute()
        )
    except APIError:
        raise HTTPException(status_code=500, detail={"message": "메시지 조회에 실패했습니다.", "code": "FETCH_FAILED"})

    # 상대방이 보낸 읽지 않은 메시지 읽음 처리
    supabase.table("messages") \
        .update({"is_read": True}) \
        .eq("connection_id", connection_id) \
        .neq("sender_id", user["id"]) \
        .eq("is_read", False) \
        .execute()

    return success_response(data=messages.data)


async def create_message(connection_id: str, body: MessageCreate, user: dict, supabase):
    conn = await get_connection_as_participant(connection_id, user, supabase)

    # 수락된 연결에서만 메시지 전송 가능
    if conn["status"] != "accepted":
        raise HTTPException(status_code=403, detail={"message": "수락된 연결에서만 메시지를 전송할 수 있습니다.", "code": "CONNECTION_NOT_ACCEPTED"})

    try:
        response = (
            supabase.table("messages")
            .insert({
                "connection_id": connection_id,
                "sender_id": user["id"],
                "content": body.content,
                "is_read": False,
            })
            .execute()
        )
    except APIError:
        raise HTTPException(status_code=500, detail={"message": "메시지 전송에 실패했습니다.", "code": "CREATE_FAILED"})

    return success_response(data=response.data[0], message="메시지를 전송했습니다.")
