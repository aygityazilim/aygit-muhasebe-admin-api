from sqlalchemy.orm import Session
from shared.repositories.base import BaseRepository
from shared.models import UserModel, AygitUserModel

class UserRepository(BaseRepository[UserModel]):
    def __init__(self, db: Session):
        super().__init__(model=UserModel, db=db)

class AygitUserRepository(BaseRepository[AygitUserModel]):
    def __init__(self, db: Session):
        super().__init__(model=AygitUserModel, db=db)