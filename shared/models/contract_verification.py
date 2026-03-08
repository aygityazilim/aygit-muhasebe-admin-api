from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from shared.models.registiration_base import RegistirationBaseModel

class ContractVerificationModel(RegistirationBaseModel):
    __tablename__ = "contract_verifications"

    link = Column(String, nullable=False)
    verification_code = Column(String, nullable=False)
    verified_code = Column(String, nullable=True)
    verification_date = Column(DateTime, nullable=True)
    sent_date = Column(DateTime, nullable=False)

    pre_registiration_id = Column(Integer, ForeignKey("pre_registirations.id"), nullable=False)
    pre_registiration = relationship("PreRegistirationModel", lazy="noload")

    def to_dict(self):
        return {
            "id": self.id,
            "link": self.link,
            "verified_code": self.verified_code,
            "verification_code": self.verification_code,
            "verification_date": self.verification_date,
            "sent_date": self.sent_date,
            "created_at": self.created_at
        }