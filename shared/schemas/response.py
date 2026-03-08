from pydantic import  Field
from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel
from uuid import UUID, uuid4
T = TypeVar('T')

class ResponseSchema(GenericModel, Generic[T]):
    id: UUID = Field(
        default_factory=uuid4,
        description="Unique identifier for this response"
    )
    status: int = Field(..., description="HTTP status code")
    success: bool = Field(..., description="Operation success status")
    error: Optional[str] = Field(None, description="Error message if any")
    data: Optional[T] = Field(None, description="Response data")

    def to_dict(self):
        return {
            "id": str(self.id),
            "status": self.status,
            "success": self.success,
            "error": self.error,
            "data": self.data 
        }