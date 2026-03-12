from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DocumentResponseSchema(BaseModel):
    id: int = Field(...)
    tax_plate: Optional[str] = Field(None)
    other: Optional[List[str]] = Field(None)
    created_at: datetime = Field(...)