from fastapi import APIRouter, Request, Response, Depends
from shared.enums import StatusCodeEnum
from shared.schemas import (
    ResponseSchema,
    LoginSchema
)
from services.auth import AuthService
from dependencies import get_auth_service

router  = APIRouter(
    prefix="/auth",
    tags=["Pre Registiration"]
)

@router.post("/login")
async def login(
    _: Request,
    response: Response,
    payload: LoginSchema,
    service: AuthService = Depends(get_auth_service)
):
    data = await service.login(payload)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data