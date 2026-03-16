from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional

class ResourceResponseSchema(BaseModel):
    id: int = Field(...)
    key: str = Field(...)
    sort_order: int = Field(...)
    is_menu: bool = Field(...)
    path: Optional[str] = Field(None)
    parent: Optional[ResourceResponseSchema] = Field(None)


ResourceResponseSchema.model_rebuild()
