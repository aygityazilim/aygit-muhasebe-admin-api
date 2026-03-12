from sqlalchemy.orm import Session
from shared.repositories.base import BaseRepository
from shared.models import RegistirationHistoryModel
from typing import List

class RegistirationHistoryRepository(BaseRepository[RegistirationHistoryModel]):
    def __init__(self, db: Session):
        super().__init__(model=RegistirationHistoryModel, db=db)

    def get_by_registiration_id(self, registiration_id: int) -> List[RegistirationHistoryModel]:
        return self.db.query(self.model).filter(
            self.model.registiration_id == registiration_id
        ).order_by(self.model.created_at.desc()).all()