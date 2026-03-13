from sqlalchemy.orm import Session
from fastapi import HTTPException
from shared.repositories import (
    RegistirationRepository,
    RegistirationHistoryRepository,
    ContractVerificationRepository
)
from shared.enums import (
    StatusCodeEnum,
    RegistirationStatusEnum
)
import random
from datetime import datetime


class ContractVerificationService:
    def __init__(self, db: Session):
        self.db = db
        self.registiration_repository = RegistirationRepository(db=db)
        self.registiration_history_repository = RegistirationHistoryRepository(db=db)
        self.contract_verification_repository = ContractVerificationRepository(db=db)

    async def send_code(self, tracking_number: str, contract_id: int) -> None:
        try:
            registiration = self.registiration_repository.get_by_field("tracking_number", tracking_number)
            if not registiration:
                raise HTTPException(status_code=404, detail="Registration not found")

            contract = self.contract_verification_repository.get_by_id(contract_id)
            if not contract:
                raise HTTPException(status_code=404, detail="Contract not found")

            if contract.registiration_id != registiration.id:
                raise HTTPException(status_code=StatusCodeEnum.BAD_REQUEST.value, detail="Contract does not belong to this registration")

            verification_code = str(random.randint(100000, 999999))
            self.contract_verification_repository.update(contract, {
                "verification_code": verification_code,
                "sent_date": datetime.now()
            })
            self.registiration_history_repository.create({
                "note": f"{contract.type} Verifikasyonu İstendi",
                "registiration_id": registiration.id,
                "status": RegistirationStatusEnum.PENDING.value
            })
            self.db.commit()
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e