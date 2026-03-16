from fastapi import APIRouter, Request, Response, Depends
from shared.enums import StatusCodeEnum
from shared.schemas import ResponseSchema
from shared.utils import JWTBearerUtil
from services.resource import ResourceService
from dependencies import get_resource_service


router = APIRouter(
    prefix="/resource",
    tags=["Resource"]
)


@router.get("/list")
async def get_list(
    request: Request,
    response: Response,
    service: ResourceService = Depends(get_resource_service),
    _ = Depends(JWTBearerUtil())
):
    data = await service.get_list()
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=data)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data
