from sqlalchemy.orm import Session
from shared.repositories.base import BaseRepository
from shared.models import ResourceModel

class ResourceRepository(BaseRepository[ResourceModel]):
    def __init__(self, db: Session):
        super().__init__(model=ResourceModel, db=db)