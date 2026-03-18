from sqlalchemy.orm import Session
from shared.repositories import (
    TicketRepository,
    TicketMessageRepository
)
from shared.schemas import (
    TicketMessageCreateSchema,
    TicketMessageResponseSchema,
    TicketResponseSchema,
    PaginationSchema
)
from shared.enums import (
    TicketMessageTypeEnum,
    TicketStatusEnum
)
from datetime import datetime
from typing import Optional, List


class TicketService:
    def __init__(self, db: Session):
        self.db = db
        self.ticket_repository = TicketRepository(db=db)
        self.ticket_message_repository = TicketMessageRepository(db=db)

    async def get(self, skip: int, limit: int, search: Optional[str]) -> PaginationSchema[TicketResponseSchema]:
        data = self.ticket_repository.get(skip, limit, search)
        return data

    async def get_one(self, uuid: str) -> TicketResponseSchema:
        ticket = self.ticket_repository.get_by_field("uuid", uuid)
        data = TicketResponseSchema(**ticket.to_dict())
        return data

    async def get_messages(self, uuid: str) -> List[TicketMessageResponseSchema]:
        ticket = self.ticket_repository.get_by_field("uuid", uuid)
        data = self.ticket_message_repository.get_by_ticket(ticket.id)
        return data

    async def answer(self, uuid: str, ticket_message_create_schema: TicketMessageCreateSchema) -> TicketResponseSchema:
        ticket = self.ticket_repository.get_by_field("uuid", uuid)
        created_message = self.ticket_message_repository.create({
            "content": ticket_message_create_schema.content,
            "type": TicketMessageTypeEnum.ANSWER.value,
            "ticket_id": ticket.id
        })
        self.ticket_repository.update(ticket, {
            "last_message_id": created_message.id,
            "last_message_date": datetime.now(),
            "status": TicketStatusEnum.ANSWERED.value
        })
        data = TicketResponseSchema(**ticket.to_dict())
        return data

    async def update_status(self, uuid: str, status: TicketStatusEnum) -> TicketResponseSchema:
        ticket = self.ticket_repository.get_by_field("uuid", uuid)
        self.ticket_repository.update(ticket, {"status": status.value})
        data = TicketResponseSchema(**ticket.to_dict())
        return data
