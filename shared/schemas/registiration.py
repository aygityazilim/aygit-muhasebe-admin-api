from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from shared.enums import RegistirationStatusEnum
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


class RegistirationResponseSchema(BaseModel):
    id: int = Field(...)
    phone: str = Field(...)
    message: str = Field(...)
    name: Optional[str] = Field(None)
    surname: Optional[str] = Field(None)
    tracking_number: str = Field(...)
    status: RegistirationStatusEnum = Field(...)
    nes_info: Optional[Dict[str, Any]] = Field(None)
    created_at: datetime = Field(...)
