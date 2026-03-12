from pydantic import BaseModel, Field
from datetime import datetime


class RegistirationHistoryResponseSchema(BaseModel):
    id: int = Field(...)
    note: str = Field(...)
    status: str = Field(...)
    created_at: datetime = Field(...)