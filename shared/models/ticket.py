from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from shared.models.aygit_base import AygitBaseModel

class TicketModel(AygitBaseModel):
    __tablename__ = "tickets"

    uuid = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)    
    status = Column(String, nullable=False)
    last_message_date = Column(DateTime, nullable=False)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    company = relationship("CompanyModel", lazy="noload")    

    last_message_id = Column(Integer, ForeignKey("ticket_messages.id"), nullable=True)
    last_message = relationship("TicketMessageModel", lazy="select", foreign_keys=[last_message_id])

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "title": self.title,
            "status": self.status,
            "last_message_date": self.last_message_date,
            "last_message": self.last_message.to_dict() if self.last_message else None,
            "created_at": self.created_at
        }