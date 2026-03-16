from pydantic import BaseModel, Field
from typing import Optional, List
from shared.schemas.resource import ResourceResponseSchema

class PackageCreateSchema(BaseModel):
    key: str = Field(...)
    name: str = Field(...)
    description: Optional[str] = Field(None)
    resource_ids:  List[int] = Field(...)

class PackageUpdateSchema(BaseModel):
    key: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    resource_ids:  Optional[List[int]] = Field(None)

class PackageResponseSchema(BaseModel):
    id: int = Field(...)
    key: str = Field(...)
    name: str = Field(...)
    description: Optional[str] = Field(None)
    resources:  List[ResourceResponseSchema] = Field(...)
