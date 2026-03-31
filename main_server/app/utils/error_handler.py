from fastapi import Request, HTTPException
from app.utils.responses import error_response
from starlette.responses import JSONResponse

async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return error_response(
            message=exc.detail,
            status_code=exc.status_code,
            details=None
        )

    return error_response(
        message="Internal Server Error",
        status_code=500,
        details=str(exc) # 개발 단계에서만 str(exc) 포함, 운영 시에는 숨김
    )