from sqlalchemy.orm import Session
from shared.repositories.base import BaseRepository
from shared.models import RegistirationModel
from shared.schemas import (
    PaginationSchema
)
from typing import Optional

class RegistirationRepository(BaseRepository[RegistirationModel]):
    def __init__(self, db: Session):
        super().__init__(model=RegistirationModel, db=db)

    def get(self, skip: int, limit: int, search: Optional[str]) -> PaginationSchema:
        query = self.db.query(self.model)
        total_count = query.count()

        if search:
            query = query.filter(
                (self.model.name.ilike(f"%{search}%")) |
                (self.model.surname.ilike(f"%{search}%")) |
                (self.model.phone.ilike(f"%{search}%")) |
                (self.model.tracking_number.ilike(f"%{search}%"))
            )

        count = query.count()
        total_pages = (count + limit - 1) // limit if limit > 0 else 1
        current_page = (skip // limit) + 1 if limit > 0 else 1

        data = query.order_by(self.model.created_at.desc()).offset(skip).limit(limit).all()

        return PaginationSchema(
            total_count=total_count,
            count=count,
            skip=skip,
            limit=limit,
            current_page=current_page,
            total_pages=total_pages,
            data=[item.to_dict() for item in data]
        )