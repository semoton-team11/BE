# messages 테이블
# - id: uuid (PK)
# - connection_id: uuid (FK → connections.id)
# - sender_id: uuid (FK → users.id)
# - content: text (메시지 내용)
# - is_read: boolean
# - created_at: timestamp
