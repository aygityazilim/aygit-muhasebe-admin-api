from sqlalchemy.orm import Session
from shared.repositories.base import BaseRepository
from shared.models import UserModel

class UserRepository(BaseRepository[UserModel]):
    def __init__(self, db: Session):
        super().__init__(model=UserModel, db=db)