from sqlalchemy.orm import Session
from shared.repositories.base import BaseRepository
from shared.models import TicketMessageModel
from shared.schemas import TicketMessageResponseSchema
from typing import List

class TicketMessageRepository(BaseRepository[TicketMessageModel]):
    def __init__(self, db: Session):
        super().__init__(model=TicketMessageModel, db=db)

    def get_by_ticket(self, ticket_id: int) -> List[TicketMessageResponseSchema]:
        items = self.db.query(self.model).filter(
            self.model.ticket_id == ticket_id,
            self.model.is_active == True
        ).order_by(self.model.created_at.desc()).all()
        return [TicketMessageResponseSchema(**item.to_dict()) for item in items]
