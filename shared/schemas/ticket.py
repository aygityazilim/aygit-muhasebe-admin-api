from pydantic import BaseModel, Field
from typing import Optional
from shared.enums import (
    TicketStatusEnum
)
from datetime import datetime
from shared.schemas.ticket_message import TicketMessageResponseSchema

class TicketCreateSchema(BaseModel):
    uuid: Optional[str] = Field(None)
    title: str = Field(...)    
    content: str = Field(...)
    status: Optional[TicketStatusEnum] = Field(TicketStatusEnum.PENDING)
    last_message_date: datetime = Field(...)
    company_id: Optional[int] = Field(None)

class TicketResponseSchema(BaseModel):
    uuid: str = Field(...)
    title: str = Field(...)
    status: TicketStatusEnum = Field(...)
    last_message_date: datetime = Field(...)
    last_message: Optional[TicketMessageResponseSchema] = Field(None)
    created_at: datetime = Field(...)
