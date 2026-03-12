from sqlalchemy.orm import Session
from shared.repositories.base import BaseRepository
from shared.models import RegistirationHistoryModel

class RegistirationHistoryRepository(BaseRepository[RegistirationHistoryModel]):
    def __init__(self, db: Session):
        super().__init__(model=RegistirationHistoryModel, db=db)