from sqlalchemy.orm import Session
from shared.repositories.base import BaseRepository
from shared.models import PreRegistirationHistoryModel

class PreRegistirationHistoryRepository(BaseRepository[PreRegistirationHistoryModel]):
    def __init__(self, db: Session):
        super().__init__(model=PreRegistirationHistoryModel, db=db)