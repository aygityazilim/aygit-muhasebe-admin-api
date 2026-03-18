from fastapi import APIRouter, Request, Response, Depends, Query
from shared.enums import StatusCodeEnum, TicketStatusEnum
from shared.schemas import (
    TicketMessageCreateSchema,
    ResponseSchema
)
from shared.utils import JWTBearerUtil
from services.ticket import TicketService
from dependencies import get_ticket_service
from typing import Optional

router = APIRouter(
    prefix="/ticket",
    tags=["Ticket"]
)


@router.get("")
async def get(
    request: Request,
    response: Response,
    skip: int = Query(0),
    limit: int = Query(10),
    search: Optional[str] = Query(None),
    service: TicketService = Depends(get_ticket_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.get(skip, limit, search)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data


@router.get("/{uuid}")
async def get_one(
    request: Request,
    response: Response,
    uuid: str,
    service: TicketService = Depends(get_ticket_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.get_one(uuid)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data


@router.get("/{uuid}/message")
async def get_messages(
    request: Request,
    response: Response,
    uuid: str,
    service: TicketService = Depends(get_ticket_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.get_messages(uuid)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data


@router.post("/{uuid}/answer")
async def answer(
    request: Request,
    response: Response,
    uuid: str,
    ticket_message_create_schema: TicketMessageCreateSchema,
    service: TicketService = Depends(get_ticket_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.answer(uuid, ticket_message_create_schema)
    data = ResponseSchema(status=StatusCodeEnum.CREATED.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.CREATED.value
    return data


@router.patch("/{uuid}/status")
async def update_status(
    request: Request,
    response: Response,
    uuid: str,
    status: TicketStatusEnum = Query(...),
    service: TicketService = Depends(get_ticket_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.update_status(uuid, status)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data
