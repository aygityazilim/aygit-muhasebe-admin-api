from fastapi import HTTPException
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
    TicketStatusEnum,
    StatusCodeEnum,
    ErrorMessageEnum
)
from datetime import datetime
from typing import Optional, List


class TicketService:
    def __init__(self, db: Session):
        self.db = db
        self.ticket_repository = TicketRepository(db=db)
        self.ticket_message_repository = TicketMessageRepository(db=db)

    async def get(self, skip: int, limit: int, search: Optional[str]) -> PaginationSchema[TicketResponseSchema]:
        try:
            data = self.ticket_repository.get(skip, limit, search)
            return data
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e

    async def get_one(self, uuid: str) -> TicketResponseSchema:
        try:
            ticket = self.ticket_repository.get_by_field("uuid", uuid)
            if not ticket:
                raise HTTPException(status_code=StatusCodeEnum.NOT_FOUND.value, detail=ErrorMessageEnum.NOT_FOUND.value)
            data = TicketResponseSchema(**ticket.to_dict())
            return data
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e

    async def get_messages(self, uuid: str) -> List[TicketMessageResponseSchema]:
        try:
            ticket = self.ticket_repository.get_by_field("uuid", uuid)
            if not ticket:
                raise HTTPException(status_code=StatusCodeEnum.NOT_FOUND.value, detail=ErrorMessageEnum.NOT_FOUND.value)
            data = self.ticket_message_repository.get_by_ticket(ticket.id)
            return data
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e

    async def answer(self, uuid: str, ticket_message_create_schema: TicketMessageCreateSchema) -> TicketResponseSchema:
        try:
            ticket = self.ticket_repository.get_by_field("uuid", uuid)
            if not ticket:
                raise HTTPException(status_code=StatusCodeEnum.NOT_FOUND.value, detail=ErrorMessageEnum.NOT_FOUND.value)
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
            self.db.commit()
            data = TicketResponseSchema(**ticket.to_dict())
            return data
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e

    async def update_status(self, uuid: str, status: TicketStatusEnum) -> TicketResponseSchema:
        try:
            ticket = self.ticket_repository.get_by_field("uuid", uuid)
            if not ticket:
                raise HTTPException(status_code=StatusCodeEnum.NOT_FOUND.value, detail=ErrorMessageEnum.NOT_FOUND.value)
            self.ticket_repository.update(ticket, {"status": status.value})
            self.db.commit()
            data = TicketResponseSchema(**ticket.to_dict())
            return data
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise e