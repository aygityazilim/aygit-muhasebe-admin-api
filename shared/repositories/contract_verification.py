from sqlalchemy.orm import Session
from shared.repositories.base import BaseRepository
from shared.models import ContractVerificationModel
from typing import List

class ContractVerificationRepository(BaseRepository[ContractVerificationModel]):
    def __init__(self, db: Session):
        super().__init__(model=ContractVerificationModel, db=db)

    def get_registiration_contracts(self, registiration_id: int) -> List[ContractVerificationModel]:
        return self.db.query(self.model).filter(self.model.registiration_id == registiration_id).all()