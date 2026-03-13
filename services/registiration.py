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
    RegistirationBaseResponseSchema,
    RegistirationResponseSchema,
    ContractVerificationResponseSchema,
    DocumentResponseSchema,
    RegistirationHistoryResponseSchema,
    PaginationSchema
)
from shared.enums import RegistirationStatusEnum, ContractVerificationTypeEnum
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

    async def create(self, payload: RegistirationCreateSchema) -> RegistirationBaseResponseSchema:
        try:
            tracking_number = str(random.randint(10**19, 10**20 - 1))
            while self.registiration_repository.get_by_field("tracking_number", tracking_number) is not None:
                tracking_number = str(random.randint(10**19, 10**20 - 1))

            payload.tracking_number = tracking_number
            payload.status = RegistirationStatusEnum.PENDING.value
            item = self.registiration_repository.create(payload.model_dump(mode="json", exclude_none=True))

            self.contract_verification_repository.create({
                "type": ContractVerificationTypeEnum.ETK.value,
                "link": "https://www.asmadanmuze.com/docs/etk-onay-metni.pdf",
                "registiration_id": item.id
            })
            self.contract_verification_repository.create({
                "type": ContractVerificationTypeEnum.KVKK.value,
                "link": "https://www.sabancivakfi.org/i/assets/documents/Sabanci-Vakfi-KVKK-Aydinlatma-Metni-Tur.pdf",
                "registiration_id": item.id
            })

            self.history_repository.create({
                "note": "Oluşturuldu",
                "status": RegistirationStatusEnum.PENDING.value,
                "registiration_id": item.id
            })
            self.db.commit()
            return RegistirationBaseResponseSchema(**item.to_dict())
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e

    async def update(self, tracking_number: str, payload: RegistirationUpdateSchema) -> RegistirationBaseResponseSchema:
        try:
            item = self.registiration_repository.get_by_field("tracking_number", tracking_number)
            if not item:
                raise HTTPException(status_code=404, detail="Pre registration not found")

            changes = []
            update_data = payload.model_dump(mode="json", exclude_none=True)

            if "status" in update_data and update_data["status"] != item.status:
                STATUS_LABELS = {
                    "pending": "Bekliyor",
                    "quoted": "Teklif Verildi",
                    "done": "Tamamlandı"
                }
                old_label = STATUS_LABELS.get(item.status, item.status)
                new_label = STATUS_LABELS.get(update_data["status"], update_data["status"])
                changes.append(f"Durum: {old_label} → {new_label}")

            if "name" in update_data and update_data["name"] != item.name:
                changes.append(f"Ad: {item.name or '—'} → {update_data['name']}")

            if "surname" in update_data and update_data["surname"] != item.surname:
                changes.append(f"Soyad: {item.surname or '—'} → {update_data['surname']}")

            if "phone" in update_data and update_data["phone"] != item.phone:
                changes.append(f"Telefon: {item.phone} → {update_data['phone']}")

            item = self.registiration_repository.update(item, update_data)

            if changes:
                self.history_repository.create({
                    "note": ", ".join(changes),
                    "status": item.status,
                    "registiration_id": item.id
                })

            self.db.commit()
            return RegistirationBaseResponseSchema(**item.to_dict())
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e

    async def delete(self, tracking_number: str) -> RegistirationBaseResponseSchema:
        try:
            item = self.registiration_repository.get_by_field("tracking_number", tracking_number)
            if not item:
                raise HTTPException(status_code=404, detail="Pre registration not found")
            data = RegistirationBaseResponseSchema(**item.to_dict())
            self.registiration_repository.delete(item.id)
            self.db.commit()
            return data
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e
