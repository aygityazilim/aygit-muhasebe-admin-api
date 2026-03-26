from pydantic import BaseModel, Field
from typing import Optional
from shared.enums import CompanyTypeEnum
from shared.schemas.package import PackageResponseSchema


class CompanyCreateSchema(BaseModel):
    full_name: str = Field(...)
    short_name: str = Field(...)
    tax_number: str = Field(...)
    tax_department: str = Field(...)
    address: str = Field(...)
    mersis_number: Optional[str] = Field(None)
    type: CompanyTypeEnum = Field(...)
    currency_id: int = Field(...)
    package_id: int = Field(...)
    is_accounting_firm: bool = Field(False)
    accounting_company_id: Optional[int] = Field(None)


class CompanyUpdateSchema(BaseModel):
    full_name: Optional[str] = Field(None)
    short_name: Optional[str] = Field(None)
    tax_number: Optional[str] = Field(None)
    tax_department: Optional[str] = Field(None)
    address: Optional[str] = Field(None)
    mersis_number: Optional[str] = Field(None)
    type: Optional[CompanyTypeEnum] = Field(None)
    package_id: Optional[int] = Field(None)
    is_accounting_firm: Optional[bool] = Field(None)
    currency_id: Optional[int] = Field(None)
    accounting_company_id: Optional[int] = Field(None)


class CompanyResponseSchema(BaseModel):
    id: int = Field(...)
    full_name: str = Field(...)
    short_name: str = Field(...)
    tax_number: str = Field(...)
    tax_department: str = Field(...)
    address: str = Field(...)
    slug: str = Field(...)
    mersis_number: Optional[str] = Field(None)
    type: str = Field(...)
    is_accounting_firm: Optional[bool] = Field(None)
    package: Optional[PackageResponseSchema] = Field(None)
    nes_username: Optional[str] = Field(None)
    environment: Optional[str] = Field(None)
    is_esmm_user: Optional[bool] = Field(None)
    is_emm_user: Optional[bool] = Field(None)
    accounting_company: Optional['CompanyResponseSchema'] = Field(None)