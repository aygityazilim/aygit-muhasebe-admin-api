from sqlalchemy import Column, String, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from shared.models.registiration_base import RegistirationBaseModel

class DocumentModel(RegistirationBaseModel):
    __tablename__ = "documents"

    tax_plate = Column(String, nullable=True)
    other = Column(JSON, nullable=True)

    registiration_id = Column(Integer, ForeignKey("registirations.id"), nullable=False)
    registiration = relationship("RegistirationModel", lazy="noload")

    def to_dict(self):
        return {
            "id": self.id,
            "tax_plate": self.tax_plate,
            "other": self.other,
            "created_at": self.created_at
        }