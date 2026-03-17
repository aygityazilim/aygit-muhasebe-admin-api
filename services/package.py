from fastapi import HTTPException
from sqlalchemy.orm import Session
from shared.repositories import PackageRepository, ResourceRepository
from shared.models import PackagesResourcesJoinModel
from shared.schemas import (
    PackageResponseSchema,
    PaginationSchema,
    ListItemSchema,
    ResourceResponseSchema,
    PackageCreateSchema, 
    PackageUpdateSchema
)
from shared.enums import (
    StatusCodeEnum,
    ErrorMessageEnum
)
from typing import Optional


class PackageService:
    def __init__(self, db: Session):
        self.db = db
        self.package_repository = PackageRepository(db=db)
        self.resource_repository = ResourceRepository(db=db)

    async def get(self, skip: int, limit: int, search: Optional[str]) -> PaginationSchema:
        return self.package_repository.get(skip, limit, search)

    async def get_list(self) -> list[ListItemSchema]:
        items = self.package_repository.get_all()
        return [
            ListItemSchema(id=item.id, name=item.name, description=item.description)
            for item in items
        ]

    async def get_one(self, id: int) -> PackageResponseSchema:
        item = self.package_repository.get_by_id(id)
        if not item:
            raise HTTPException(status_code=StatusCodeEnum.NOT_FOUND.value, detail=ErrorMessageEnum.NOT_FOUND.value)

        return PackageResponseSchema(
            id=item.id,
            key=item.key,
            name=item.name,
            description=item.description,
            resources=[
                ResourceResponseSchema(**r.resource.to_dict())
                for r in item.resources
            ]
        )

    async def create(self, payload: PackageCreateSchema) -> PackageResponseSchema:
        try:
            package = self.package_repository.create({
                "key": payload.key,
                "name": payload.name,
                "description": payload.description,
            })

            for resource_id in payload.resource_ids:
                join = PackagesResourcesJoinModel(
                    package_id=package.id,
                    resource_id=resource_id,
                )
                self.db.add(join)

            self.db.flush()
            self.db.refresh(package)
            self.db.commit()

            return PackageResponseSchema(
                id=package.id,
                key=package.key,
                name=package.name,
                description=package.description,
                resources=[
                    ResourceResponseSchema(**r.resource.to_dict())
                    for r in package.resources
                ]
            )
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e

    async def update(self, id: int, payload: PackageUpdateSchema) -> PackageResponseSchema:
        try:
            package = self.package_repository.get_by_id(id)
            if not package:
                raise HTTPException(status_code=StatusCodeEnum.NOT_FOUND.value, detail=ErrorMessageEnum.NOT_FOUND.value)

            update_data = payload.model_dump(mode="json", exclude_none=True, exclude={"resource_ids"})
            if update_data:
                package = self.package_repository.update(package, update_data)

            if payload.resource_ids is not None:
                existing_resource_ids = {r.resource_id for r in package.resources}
                new_resource_ids = set(payload.resource_ids)

                
                to_remove = existing_resource_ids - new_resource_ids
                if to_remove:
                    self.db.query(PackagesResourcesJoinModel).filter(
                        PackagesResourcesJoinModel.package_id == package.id,
                        PackagesResourcesJoinModel.resource_id.in_(to_remove)
                    ).delete(synchronize_session="fetch")


                to_add = new_resource_ids - existing_resource_ids
                for resource_id in to_add:
                    join = PackagesResourcesJoinModel(
                        package_id=package.id,
                        resource_id=resource_id,
                    )
                    self.db.add(join)

                self.db.flush()
                self.db.refresh(package)

            self.db.commit()

            return PackageResponseSchema(
                id=package.id,
                key=package.key,
                name=package.name,
                description=package.description,
                resources=[
                    ResourceResponseSchema(**r.resource.to_dict())
                    for r in package.resources
                ]
            )
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e

    async def delete(self, id: int) -> PackageResponseSchema:
        try:
            package = self.package_repository.get_by_id(id)
            if not package:
                raise HTTPException(status_code=StatusCodeEnum.NOT_FOUND.value, detail=ErrorMessageEnum.NOT_FOUND.value)

            data = PackageResponseSchema(
                id=package.id,
                key=package.key,
                name=package.name,
                description=package.description,
                resources=[
                    ResourceResponseSchema(**r.resource.to_dict())
                    for r in package.resources
                ]
            )
            self.package_repository.delete(package.id)
            self.db.commit()
            return data
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e
