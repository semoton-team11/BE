from typing import Any, Optional
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(
    data: Any = None, 
    message: str = "Success", 
    status_code: int = 200
):
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder({
            "status": "success",
            "message": message,
            "data": data
        })
    )

def error_response(
    message: str = "Error occurred", 
    status_code: int = 400, 
    code: Optional[str] = None, # 비즈니스 에러 코드 추가
    details: Any = None
):
    response_content = {
        "status": "error",
        "message": message,
        "details": details
    }
    if code:
        response_content["code"] = code
        
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(response_content)
    )