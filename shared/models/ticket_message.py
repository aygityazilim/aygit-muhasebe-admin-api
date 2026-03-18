from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from shared.models.aygit_base import AygitBaseModel

class TicketMessageModel(AygitBaseModel):
    __tablename__ = "ticket_messages"

    content = Column(String, nullable=False)
    type = Column(String, nullable=False)

    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    ticket = relationship("TicketModel", lazy="noload", foreign_keys=[ticket_id])

    def to_dict(self):
        return {
            "content": self.content,
            "type": self.type,
            "created_at": self.created_at
        }