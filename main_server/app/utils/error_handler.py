from fastapi import Request
from app.utils.responses import error_response

async def global_exception_handler(request: Request, exc: Exception):
    return error_response(
        message="Internal Server Error",
        status_code=500,
        details=str(exc)
    )