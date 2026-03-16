from pydantic import BaseModel, Field
from typing import Optional, Any

class ListItemSchema(BaseModel):
    id: int = Field(...)
    uuid: Optional[str] = Field(None)
    name: str = Field(...)
    description: Optional[str]  = Field(None)
    slug: Optional[str] = Field(None)
    metadata: Optional[Any] = Field(None)
    image: Optional[str] = Field(None)