from sqlalchemy.orm import Session
from shared.repositories.base import BaseRepository
from shared.models import CompanyModel

class CompanyRepository(BaseRepository[CompanyModel]):
    def __init__(self, db: Session):
        super().__init__(model=CompanyModel, db=db)