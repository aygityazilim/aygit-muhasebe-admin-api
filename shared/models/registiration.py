from sqlalchemy import Column, String, JSON, Integer, Boolean
from shared.models.registiration_base import RegistirationBaseModel

class RegistirationModel(RegistirationBaseModel):
    __tablename__ = "registirations"

    phone = Column(String, nullable=False, unique=True)
    message = Column(String, nullable=False)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    tracking_number = Column(String, nullable=False, unique=True)
    status = Column(String, nullable=False)
    nes_info = Column(JSON, nullable=True)
    aygit_company_id = Column(Integer, nullable=True)


    def to_dict(self):
        return {
            "id": self.id,
            "phone": self.phone,
            "message": self.message,
            "name": self.name,
            "surname": self.surname,
            "tracking_number": self.tracking_number,
            "status": self.status,
            "nes_info": self.nes_info,
            "aygit_company_id": self.aygit_company_id,
            "created_at": self.created_at
        }
