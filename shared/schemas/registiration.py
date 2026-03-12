from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List
from shared.enums import RegistirationStatusEnum
from shared.schemas.contract_verification import ContractVerificationResponseSchema
from shared.schemas.document import DocumentResponseSchema
from shared.schemas.registiration_history import RegistirationHistoryResponseSchema
from datetime import datetime


class RegistirationCreateSchema(BaseModel):
    phone: str = Field(...)
    message: str = Field(...)
    name: Optional[str] = Field(None)
    surname: Optional[str] = Field(None)
    tracking_number: Optional[str] = Field(None)
    status: Optional[RegistirationStatusEnum] = Field(None)


class RegistirationUpdateSchema(BaseModel):
    phone: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    surname: Optional[str] = Field(None)
    status: Optional[RegistirationStatusEnum] = Field(None)


class RegistirationBaseResponseSchema(BaseModel):
    id: int = Field(...)
    phone: str = Field(...)
    message: str = Field(...)
    name: Optional[str] = Field(None)
    surname: Optional[str] = Field(None)
    tracking_number: str = Field(...)
    status: RegistirationStatusEnum = Field(...)
    nes_info: Optional[Dict[str, Any]] = Field(None)
    created_at: datetime = Field(...)


class RegistirationResponseSchema(RegistirationBaseResponseSchema):
    contracts: List[ContractVerificationResponseSchema] = Field(...)
    document: Optional[DocumentResponseSchema] = Field(None)
    history: List[RegistirationHistoryResponseSchema] = Field(...)
