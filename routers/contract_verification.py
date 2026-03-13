from fastapi import APIRouter, Request, Response, Depends, Query
from shared.enums import StatusCodeEnum
from shared.schemas import ResponseSchema
from shared.utils import JWTBearerUtil
from services.contract_verification import ContractVerificationService
from dependencies import get_contract_verification_service


router = APIRouter(
    prefix="/contract-verification",
    tags=["Contract Verification"]
)


@router.patch("/{tracking_number}/send-code")
async def send_code(
    request: Request,
    response: Response,
    tracking_number: str,
    contract: int = Query(...),
    service: ContractVerificationService = Depends(get_contract_verification_service),
    _ = Depends(JWTBearerUtil())
):
    await service.send_code(tracking_number, contract)
    data = ResponseSchema(status=StatusCodeEnum.SUCCESS.value, success=True, error=None, data=None)
    response.status_code = StatusCodeEnum.SUCCESS.value
    return data