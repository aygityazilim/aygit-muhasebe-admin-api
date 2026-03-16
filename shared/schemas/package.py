from pydantic import BaseModel, Field
from typing import Optional, List
from shared.schemas.resource import ResourceResponseSchema

class PackageCreateSchema(BaseModel):
    key: str = Field(...)
    name: str = Field(...)
    description: Optional[str] = Field(None)
    resource_ids:  List[int] = Field(...)

class PackageResponseSchema(BaseModel):
    key: str = Field(...)
    name: str = Field(...)
    description: Optional[str] = Field(None)
    resources:  List[ResourceResponseSchema] = Field(...)
