from fastapi import HTTPException
from app.utils.responses import success_response
from app.services.common import get_connection_as_participant

MESSAGE_COLUMNS = "id, connection_id, sender_id, content, is_read, created_at"


async def read_messages(connection_id: str, user: dict, supabase):
    conn = await get_connection_as_participant(connection_id, user, supabase)

    # 수락된 연결에서만 메시지 조회 가능
    if conn["status"] != "accepted":
        raise HTTPException(status_code=403, detail={"message": "수락된 연결에서만 메시지를 조회할 수 있습니다.", "code": "CONNECTION_NOT_ACCEPTED"})

    messages = (
        supabase.table("messages")
        .select(MESSAGE_COLUMNS)
        .eq("connection_id", connection_id)
        .order("created_at", desc=False)
        .execute()
    )

    return success_response(data=messages.data)
