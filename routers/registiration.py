from fastapi import APIRouter, Request, Response, Depends
from shared.enums import StatusCodeEnum
from shared.schemas import (
    ResponseSchema,
    PreRegistirationCreateSchema,
    PreRegistirationUpdateSchema
)
from services.registiration import RegistirationService
from dependencies import get_registiration_service

router = APIRouter(
    prefix="/registiration",
    tags=["Registiration"]
)


@router.get("/list")
async def get_list(
    request: Request,
    response: Response,
    service: RegistirationService = Depends(get_registiration_service)
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
    service: RegistirationService = Depends(get_registiration_service)
):
    data = await service.get_one(tracking_number)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data


@router.post("/")
async def create(
    request: Request,
    response: Response,
    payload: PreRegistirationCreateSchema,
    service: RegistirationService = Depends(get_registiration_service)
):
    data = await service.create(payload)
    data = ResponseSchema(status=StatusCodeEnum.CREATED.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.CREATED.value
    return data


@router.put("/{tracking_number}")
async def update(
    request: Request,
    response: Response,
    tracking_number: str,
    payload: PreRegistirationUpdateSchema,
    service: RegistirationService = Depends(get_registiration_service)
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
    service: RegistirationService = Depends(get_registiration_service)
):
    await service.delete(tracking_number)
    data = ResponseSchema(status=StatusCodeEnum.NO_CONTENT.value, success=True, error=None, data=None)
    response.status_code = StatusCodeEnum.NO_CONTENT.value
    return data
