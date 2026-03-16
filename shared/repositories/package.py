from sqlalchemy.orm import Session
from shared.repositories.base import BaseRepository
from shared.models import PackageModel

class PackageRepository(BaseRepository[PackageModel]):
    def __init__(self, db: Session):
        super().__init__(model=PackageModel, db=db)