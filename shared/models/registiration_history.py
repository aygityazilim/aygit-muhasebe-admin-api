from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from shared.models.registiration_base import RegistirationBaseModel

class RegistirationHistoryModel(RegistirationBaseModel):
    __tablename__ = "registiration_histories"

    note = Column(String, nullable=False)
    status = Column(String, nullable=False)

    registiration_id = Column(Integer, ForeignKey("registirations.id"), nullable=False)
    registiration = relationship("RegistirationModel", lazy="noload")

    def to_dict(self):
        return {
            "id": self.id,
            "note": self.note,
            "status": self.status,            
            "created_at": self.created_at
        }