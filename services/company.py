from fastapi import HTTPException
from sqlalchemy.orm import Session
from shared.repositories import CompanyRepository, PackageRepository, AygitUserRepository, UsersResourcesJoinRepository
from shared.schemas import (
    PaginationSchema, 
    ListItemSchema,
    CompanyCreateSchema, 
    CompanyUpdateSchema, 
    CompanyResponseSchema,
    PackageResponseSchema,
    ResourceResponseSchema,
    CreateCompanyUserSchema
) 
from shared.enums import (
    StatusCodeEnum,
    ErrorMessageEnum
)
from shared.utils import (
    PasswordUtil,
    EmailUtils
)
from typing import Optional, List
from slugify import slugify
import random


def _build_response(company) -> CompanyResponseSchema:
    package_data = None
    if company.package:
        pkg = company.package
        package_data = PackageResponseSchema(
            id=pkg.id,
            key=pkg.key,
            name=pkg.name,
            description=pkg.description,
            resources=[
                ResourceResponseSchema(**r.resource.to_dict())
                for r in pkg.resources
            ]
        )

    accounting_company_data = None
    if company.accounting_company:
        accounting_company_data = CompanyResponseSchema(
            **{k: v for k, v in company.accounting_company.to_dict().items() if k in CompanyResponseSchema.model_fields}
        )

    return CompanyResponseSchema(
        id=company.id,
        logo=company.logo,
        title=company.title,
        tax_number=company.tax_number,
        tax_department=company.tax_department,
        address=company.address,
        district=company.district,
        city=company.city,
        country=company.country,
        name=company.name,
        surname=company.surname,
        postal_code=company.postal_code,
        phone=company.phone,
        fax=company.fax,
        mail=company.mail,
        web_site=company.web_site,
        slug=company.slug,
        type=company.type,
        is_accounting_firm=company.is_accounting_firm,
        package=package_data,
        nes_username=company.nes_username,
        environment=company.environment,
        is_esmm_user=company.is_esmm_user,
        is_emm_user=company.is_emm_user,
        accounting_company=accounting_company_data,
    )


class CompanyService:
    def __init__(self, db: Session):
        self.db = db
        self.company_repository = CompanyRepository(db=db)
        self.package_repository = PackageRepository(db=db)
        self.aygit_user_repository = AygitUserRepository(db=db)
        self.users_resources_join_repository = UsersResourcesJoinRepository(db=db)

    async def get(self, skip: int, limit: int, search: Optional[str]) -> PaginationSchema:
        result = self.company_repository.get(skip, limit, search)
        result.data = [_build_response(item) for item in result.data]
        return result

    async def get_list(self) -> List[ListItemSchema]:
        items = self.company_repository.get_all()
        return [
            ListItemSchema(
                id=item.id,
                name=item.title,
                description=item.city,
                slug=item.slug,
            )
            for item in items
        ]

    async def get_one(self, id: int) -> CompanyResponseSchema:
        item = self.company_repository.get_by_id(id)
        if not item:
            raise HTTPException(status_code=404, detail="Company not found")
        return _build_response(item)

    async def create(self, payload: CompanyCreateSchema) -> CompanyResponseSchema:
        try:
            existing = self.company_repository.get_by_field("tax_number", payload.tax_number)
            if existing:
                raise HTTPException(status_code=400, detail="Company with this tax number already exists")

            slug = slugify(payload.title)
            existing_company = self.company_repository.get_by_field("slug", slug)
            while existing_company is not None:
                new_slug = f"{slug}{random.randint(100000, 999999)}"
                existing_company = self.company_repository.get_by_field("slug", new_slug)
                if existing_company is None:
                    slug = new_slug

            data = payload.model_dump(mode="json")
            data["slug"] = slug
            if data.get("type"):
                data["type"] = data["type"]

            company = self.company_repository.create(data)
            self.db.commit()
            self.db.refresh(company)
            return _build_response(company)
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e

    async def update(self, id: int, payload: CompanyUpdateSchema) -> CompanyResponseSchema:
        try:
            company = self.company_repository.get_by_id(id)
            if not company:
                raise HTTPException(status_code=404, detail="Company not found")

            update_data = payload.model_dump(mode="json", exclude_none=True)

            if "title" in update_data and update_data["title"] != company.title:
                slug = slugify(update_data["title"])
                existing_company = self.company_repository.get_by_field("slug", slug)
                while existing_company is not None and existing_company.id != company.id:
                    new_slug = f"{slug}{random.randint(100000, 999999)}"
                    existing_company = self.company_repository.get_by_field("slug", new_slug)
                    if existing_company is None or existing_company.id == company.id:
                        slug = new_slug
                update_data["slug"] = slug

            company = self.company_repository.update(company, update_data)
            self.db.commit()
            self.db.refresh(company)
            return _build_response(company)
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e

    async def delete(self, id: int) -> CompanyResponseSchema:
        try:
            company = self.company_repository.get_by_id(id)
            if not company:
                raise HTTPException(status_code=404, detail="Company not found")

            data = _build_response(company)
            self.company_repository.delete(company.id)
            self.db.commit()
            return data
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e
        
    async def get_accounting_companies(self, search: Optional[str]) -> List[ListItemSchema]:
        try:
            data = self.company_repository.get_accounting_companies(search)
            return [
                ListItemSchema(
                    id=company.id,
                    name=company.title,
                    slug=company.slug,
                    image=company.logo
                ) for company in data
            ]
        except HTTPException:
            raise
        except Exception as e:
            raise e

    async def create_user(self, payload: CreateCompanyUserSchema) -> None:
        try:
            existing_user = self.aygit_user_repository.get_by_field("email", payload.email)
            if existing_user:
                raise HTTPException(status_code=StatusCodeEnum.BAD_REQUEST.value, detail=ErrorMessageEnum.USER_EXISTS.value)
            password = PasswordUtil.generate_password(12)
            payload.password = PasswordUtil.hash(password)
            company = self.company_repository.get_by_id(payload.company_id)
            user = self.aygit_user_repository.create(payload.model_dump(mode="json"))
            users_resources = []
            for pr in company.package.resources:
                users_resources.append({"user_id": user.id, "resource_id": pr.resource_id})
            self.users_resources_join_repository.bulk_create(users_resources)
            await EmailUtils.send_email("user.html", "Aygıt Muhasebe Giriş Bilgileri", payload.email, email=payload.email, name=user.name, surname=user.surname, password=password)
            self.db.commit()
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e