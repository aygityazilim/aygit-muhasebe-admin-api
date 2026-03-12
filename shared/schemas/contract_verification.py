from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from shared.enums import ContractVerificationTypeEnum

class ContractVerificationResponseSchema(BaseModel):
    id: int = Field(...)
    link: str = Field(...)
    verified_code: Optional[str] = Field(None)
    verification_code: Optional[str] = Field(None)
    verification_date: Optional[datetime] = Field(None)
    type: ContractVerificationTypeEnum = Field(...)
    sent_date: Optional[datetime] = Field(None)
    created_at: datetime = Field(...)