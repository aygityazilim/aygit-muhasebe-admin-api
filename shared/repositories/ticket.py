from sqlalchemy.orm import Session
from shared.repositories.base import BaseRepository
from shared.models import TicketModel
from shared.schemas import PaginationSchema, TicketResponseSchema
from typing import Optional

class TicketRepository(BaseRepository[TicketModel]):
    def __init__(self, db: Session):
        super().__init__(model=TicketModel, db=db)

    def get(self, skip: int, limit: int, search: Optional[str]) -> PaginationSchema[TicketResponseSchema]:
        query = self.db.query(self.model).filter(self.model.is_active == True)
        total_count = query.count()

        if search:
            query = query.filter(self.model.title.ilike(f"%{search}%"))

        count = query.count()
        total_pages = (count + limit - 1) // limit if limit > 0 else 1
        current_page = (skip // limit) + 1 if limit > 0 else 1

        data = query.order_by(self.model.last_message_date.desc()).offset(skip).limit(limit).all()
        data = [TicketResponseSchema(**item.to_dict()) for item in data]

        return PaginationSchema(
            total_count=total_count,
            count=count,
            skip=skip,
            limit=limit,
            current_page=current_page,
            total_pages=total_pages,
            data=data
        )
