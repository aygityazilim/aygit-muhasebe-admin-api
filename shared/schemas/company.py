from pydantic import BaseModel, Field
from typing import Optional
from shared.enums import CompanyTypeEnum

class CompanyCreateSchema(BaseModel):     
    full_name: str = Field(...)
    short_name: str = Field(...)
    tax_number: str = Field(...)
    tax_department: str = Field(...)    
    address: str = Field(...)    
    mersis_number: Optional[str] = Field(None)
    type: CompanyTypeEnum = Field(...)
    package_id: int = Field(...)