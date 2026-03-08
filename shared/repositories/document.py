from sqlalchemy.orm import Session
from shared.repositories.base import BaseRepository
from shared.models import DocumentModel

class DocumentRepository(BaseRepository[DocumentModel]):
    def __init__(self, db: Session):
        super().__init__(model=DocumentModel, db=db)