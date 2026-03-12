from pydantic import  Field
from typing import Generic, List, TypeVar
from pydantic.generics import GenericModel

T = TypeVar('T')

class PaginationSchema(GenericModel, Generic[T]):   


    total_count: int = Field(..., description="Total count of the data")
    count: int = Field(..., description="Filtered count")
    skip: int = Field(..., description="Skip amount")
    limit: int = Field(..., description="Limit amount")
    current_page: int = Field(..., description="Current page")
    total_pages: int = Field(..., description="Filtered total pages")
    data: List[T] = Field(..., description="Response data")