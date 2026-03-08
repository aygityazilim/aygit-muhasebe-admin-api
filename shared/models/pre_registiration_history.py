from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from shared.models.registiration_base import RegistirationBaseModel

class PreRegistirationHistoryModel(RegistirationBaseModel):
    __tablename__ = "pre_registiration_histories"

    note = Column(String, nullable=False)
    status = Column(String, nullable=False)

    pre_registiration_id = Column(Integer, ForeignKey("pre_registirations.id"), nullable=False)
    pre_registiration = relationship("PreRegistirationModel", lazy="noload")

    def to_dict(self):
        return {
            "id": self.id,
            "note": self.note,
            "status": self.status,            
            "created_at": self.created_at
        }