from sqlalchemy.orm import Session
from shared.repositories.base import BaseRepository
from shared.models import UsersResourcesJoinModel

class UsersResourcesJoinRepository(BaseRepository[UsersResourcesJoinModel]):
    def __init__(self, db: Session):
        super().__init__(model=UsersResourcesJoinModel, db=db)