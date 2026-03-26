from pydantic import BaseModel, Field

class ResourceResponseSchema(BaseModel):
    id: int = Field(...)
    key: str = Field(...)
