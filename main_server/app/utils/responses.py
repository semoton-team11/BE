from typing import Any
from fastapi.responses import JSONResponse

def success_response(data: Any = None, message: str = "Success", status_code: int = 200):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success",
            "message": message,
            "data": data
        }
    )

def error_response(message: str = "Error occurred", status_code: int = 400, details: Any = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message,
            "details": details
        }
    )