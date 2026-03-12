from fastapi import HTTPException
from sqlalchemy.orm import Session
from shared.repositories import (
    RegistirationRepository,
    ContractVerificationRepository,
    DocumentRepository,
    RegistirationHistoryRepository
)
from shared.schemas import (
    RegistirationCreateSchema,
    RegistirationUpdateSchema,
    RegistirationResponseSchema,
    ContractVerificationResponseSchema,
    DocumentResponseSchema,
    RegistirationHistoryResponseSchema,
    PaginationSchema
)
from shared.enums import RegistirationStatusEnum
import random
from typing import Optional


class RegistirationService:
    def __init__(self, db: Session):
        self.db = db
        self.registiration_repository = RegistirationRepository(db=db)
        self.contract_verification_repository = ContractVerificationRepository(db=db)
        self.document_repository = DocumentRepository(db=db)
        self.history_repository = RegistirationHistoryRepository(db=db)

    async def get(self, skip: int, limit: int, search: Optional[str]) -> PaginationSchema[RegistirationResponseSchema]:
        data = self.registiration_repository.get(skip, limit, search)
        return data

    async def get_list(self):
        items = self.registiration_repository.get_all()
        return [RegistirationResponseSchema(**item.to_dict()) for item in items]

    async def get_one(self, tracking_number: str) -> RegistirationResponseSchema:
        registiration = self.registiration_repository.get_by_field("tracking_number", tracking_number)
        if not registiration:
            raise HTTPException(status_code=404, detail="Pre registration not found")

        contracts = self.contract_verification_repository.get_registiration_contracts(registiration.id)
        document = self.document_repository.get_by_field("registiration_id", registiration.id)

        data = registiration.to_dict()
        data["contracts"] = [ContractVerificationResponseSchema(**contract.to_dict()) for contract in contracts]
        data["document"] = DocumentResponseSchema(**document.to_dict()) if document else None

        history = self.history_repository.get_by_registiration_id(registiration.id)
        data["history"] = [RegistirationHistoryResponseSchema(**h.to_dict()) for h in history]

        return data

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
