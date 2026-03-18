from pydantic import BaseModel, Field
from shared.enums import TicketMessageTypeEnum
from datetime import datetime
from typing import Optional

class TicketMessageCreateSchema(BaseModel):
    content: str = Field(...)
    type: Optional[TicketMessageTypeEnum] = Field(None)

class TicketMessageResponseSchema(BaseModel):
    content: str = Field(...)
    type: TicketMessageTypeEnum = Field(...)
    created_at: datetime = Field(...)