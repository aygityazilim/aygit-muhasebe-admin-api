from fastapi import HTTPException
from sqlalchemy.orm import Session
from shared.repositories import RegistirationRepository
from shared.schemas import (
    RegistirationCreateSchema,
    RegistirationUpdateSchema,
    RegistirationResponseSchema,
    PaginationSchema
)
from shared.enums import RegistirationStatusEnum
import random
from typing import Optional


class RegistirationService:
    def __init__(self, db: Session):
        self.db = db
        self.registiration_repository = RegistirationRepository(db=db)

    async def get(self, skip: int, limit: int, search: Optional[str]) -> PaginationSchema[RegistirationResponseSchema]:        
        data = self.registiration_repository.get(skip, limit, search)
        return data

    async def get_list(self):
        items = self.repository.get_all()
        return [RegistirationResponseSchema(**item.to_dict()) for item in items]

    async def get_one(self, tracking_number: str) -> RegistirationResponseSchema:
        item = self.repository.get_by_field("tracking_number", tracking_number)
        if not item:
            raise HTTPException(status_code=404, detail="Pre registration not found")
        return RegistirationResponseSchema(**item.to_dict())

    async def create(self, payload: RegistirationCreateSchema) -> RegistirationResponseSchema:
        try:
            tracking_number = str(random.randint(10**19, 10**20 - 1))
            while self.repository.get_by_field("tracking_number", tracking_number) is not None:
                tracking_number = str(random.randint(10**19, 10**20 - 1))

            payload.tracking_number = tracking_number
            payload.status = RegistirationStatusEnum.PENDING.value
            item = self.repository.create(payload.model_dump(mode="json", exclude_none=True))
            self.db.commit()
            return RegistirationResponseSchema(**item.to_dict())
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e

    async def update(self, tracking_number: str, payload: RegistirationUpdateSchema) -> RegistirationResponseSchema:
        try:
            item = self.repository.get_by_field("tracking_number", tracking_number)
            if not item:
                raise HTTPException(status_code=404, detail="Pre registration not found")
            item = self.repository.update(item, payload.model_dump(mode="json", exclude_none=True))
            self.db.commit()
            return RegistirationResponseSchema(**item.to_dict())
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e

    async def delete(self, tracking_number: str):
        try:
            item = self.repository.get_by_field("tracking_number", tracking_number)
            if not item:
                raise HTTPException(status_code=404, detail="Pre registration not found")
            self.repository.delete(item.id)
            self.db.commit()
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e
