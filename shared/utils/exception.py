from fastapi.exceptions import RequestValidationError
from shared.schemas import ResponseSchema
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

def http_exception_handler(_: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=ResponseSchema(status=exc.status_code, error=exc.detail, data=None, success=False).to_dict())  

def request_validation_exception_handler(_: Request, exc: RequestValidationError):
     return JSONResponse(
        status_code=422,
        content=ResponseSchema(
            status=422,
            error=str(exc),  
            success=False,
            data=None
        ).to_dict()
    )

def internal_server_exception_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ResponseSchema(
            status=500,
            error=str(exc), 
            success=False,
            data=None
        ).to_dict()
    )