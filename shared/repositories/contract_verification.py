from sqlalchemy.orm import Session
from shared.repositories.base import BaseRepository
from shared.models import ContractVerificationModel

class ContractVerificationRepository(BaseRepository[ContractVerificationModel]):
    def __init__(self, db: Session):
        super().__init__(model=ContractVerificationModel, db=db)