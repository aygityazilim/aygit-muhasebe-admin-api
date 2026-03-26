from pydantic import BaseModel, Field
from typing import Optional
from shared.enums import (
    CompanyTypeEnum,
    RoleEnum
)
from shared.schemas.package import PackageResponseSchema


class CompanyCreateSchema(BaseModel):
    title: str = Field(...)
    tax_number: str = Field(...)
    tax_department: Optional[str] = Field(None)
    address: str = Field(...)
    district: str = Field(...)
    city: str = Field(...)
    country: str = Field(...)
    name: Optional[str] = Field(None)
    surname: Optional[str] = Field(None)
    postal_code: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    fax: Optional[str] = Field(None)
    mail: Optional[str] = Field(None)
    web_site: Optional[str] = Field(None)
    type: CompanyTypeEnum = Field(...)
    currency_id: int = Field(...)
    package_id: int = Field(...)
    is_accounting_firm: bool = Field(False)
    accounting_company_id: Optional[int] = Field(None)


class CompanyUpdateSchema(BaseModel):
    title: Optional[str] = Field(None)
    tax_number: Optional[str] = Field(None)
    tax_department: Optional[str] = Field(None)
    address: Optional[str] = Field(None)
    district: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    country: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    surname: Optional[str] = Field(None)
    postal_code: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    fax: Optional[str] = Field(None)
    mail: Optional[str] = Field(None)
    web_site: Optional[str] = Field(None)
    type: Optional[CompanyTypeEnum] = Field(None)
    package_id: Optional[int] = Field(None)
    is_accounting_firm: Optional[bool] = Field(None)
    currency_id: Optional[int] = Field(None)
    accounting_company_id: Optional[int] = Field(None)


class CompanyResponseSchema(BaseModel):
    id: int = Field(...)
    logo: Optional[str] = Field(None)
    title: str = Field(...)
    tax_number: str = Field(...)
    tax_department: Optional[str] = Field(None)
    address: str = Field(...)
    district: str = Field(...)
    city: str = Field(...)
    country: str = Field(...)
    name: Optional[str] = Field(None)
    surname: Optional[str] = Field(None)
    postal_code: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    fax: Optional[str] = Field(None)
    mail: Optional[str] = Field(None)
    web_site: Optional[str] = Field(None)
    slug: str = Field(...)
    type: str = Field(...)
    is_accounting_firm: Optional[bool] = Field(None)
    package: Optional[PackageResponseSchema] = Field(None)
    nes_username: Optional[str] = Field(None)
    environment: Optional[str] = Field(None)
    is_esmm_user: Optional[bool] = Field(None)
    is_emm_user: Optional[bool] = Field(None)
    accounting_company: Optional['CompanyResponseSchema'] = Field(None)

class CreateCompanyUserSchema(BaseModel):    
    name: str = Field(...)
    surname: str = Field(...)
    email: str = Field(...)
    phone: str = Field(...)
    company_id: int = Field(...)
    role: Optional[RoleEnum] = Field(RoleEnum.ACCOUNT_OWNER)
    password: Optional[str] = Field(None)