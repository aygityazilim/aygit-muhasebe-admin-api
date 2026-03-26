from fastapi import APIRouter, Request, Response, Depends, Query
from shared.enums import StatusCodeEnum
from shared.schemas import ResponseSchema
from shared.schemas.company import CompanyCreateSchema, CompanyUpdateSchema
from shared.utils import JWTBearerUtil
from services.company import CompanyService
from dependencies import get_company_service
from typing import Optional


router = APIRouter(
    prefix="/company",
    tags=["Company"]
)


@router.get("")
async def get(
    request: Request,
    response: Response,
    skip: int,
    limit: int,
    search: Optional[str] = Query(None),
    service: CompanyService = Depends(get_company_service),
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
    service: CompanyService = Depends(get_company_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.get_list()
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data


@router.get("/accounting")
async def get_accounting_companies(
    request: Request,
    response: Response,
    search: Optional[str] = Query(None),
    service: CompanyService = Depends(get_company_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.get_accounting_companies(search)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data


@router.get("/{id}")
async def get_one(
    request: Request,
    response: Response,
    id: int,
    service: CompanyService = Depends(get_company_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.get_one(id)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data


@router.post("")
async def create(
    request: Request,
    response: Response,
    payload: CompanyCreateSchema,
    service: CompanyService = Depends(get_company_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.create(payload)
    data = ResponseSchema(status=StatusCodeEnum.CREATED.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.CREATED.value
    return data


@router.patch("/{id}")
async def update(
    request: Request,
    response: Response,
    id: int,
    payload: CompanyUpdateSchema,
    service: CompanyService = Depends(get_company_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.update(id, payload)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data


@router.delete("/{id}")
async def delete(
    request: Request,
    response: Response,
    id: int,
    service: CompanyService = Depends(get_company_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.delete(id)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data