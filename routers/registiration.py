from fastapi import APIRouter, Request, Response, Depends, Query
from shared.enums import StatusCodeEnum
from typing import Optional
from shared.schemas import (
    ResponseSchema,
    RegistirationCreateSchema,
    RegistirationUpdateSchema
)
from shared.utils import (
    JWTBearerUtil
)
from services.registiration import RegistirationService
from dependencies import get_registiration_service


router = APIRouter(
    prefix="/registiration",
    tags=["Registiration"]
)

@router.get("")
async def get(
    request: Request,
    response: Response,
    skip: int,
    limit: int,
    search: Optional[str] = Query(None),
    service: RegistirationService = Depends(get_registiration_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.get(skip, limit, search)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data


@router.get("/list")
async def get_list(
    request: Request,
    response: Response,
    service: RegistirationService = Depends(get_registiration_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.get_list()
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data


@router.get("/{tracking_number}")
async def get_one(
    request: Request,
    response: Response,
    tracking_number: str,
    service: RegistirationService = Depends(get_registiration_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.get_one(tracking_number)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data


@router.post("/")
async def create(
    request: Request,
    response: Response,
    payload: RegistirationCreateSchema,
    service: RegistirationService = Depends(get_registiration_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.create(payload)
    data = ResponseSchema(status=StatusCodeEnum.CREATED.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.CREATED.value
    return data


@router.patch("/{tracking_number}")
async def update(
    request: Request,
    response: Response,
    tracking_number: str,
    payload: RegistirationUpdateSchema,
    service: RegistirationService = Depends(get_registiration_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.update(tracking_number, payload)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data


@router.delete("/{tracking_number}")
async def delete(
    request: Request,
    response: Response,
    tracking_number: str,
    service: RegistirationService = Depends(get_registiration_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.delete(tracking_number)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data
