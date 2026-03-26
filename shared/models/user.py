from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from shared.models.base import BaseModel
from shared.models.aygit_base import AygitBaseModel

class UserModel(BaseModel):
    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    def to_dict(self):
        return {
            "email": self.email,
            "password": self.password,
            "name": self.name,
            "surname": self.surname
        }
    



class AygitUserModel(AygitBaseModel):
    __tablename__ = "users"

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    role = Column(String, nullable=False)
    email_verified = Column(Boolean, nullable=False, default=True)

    email_verification_code = Column(String, nullable=True)
    email_verification_code_sent_at = Column(DateTime, nullable=True)

    password_reset_code = Column(String, nullable=True)
    password_reset_code_sent_at = Column(DateTime, nullable=True)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    company = relationship("CompanyModel", foreign_keys=[company_id], lazy="joined")

    resources = relationship("UsersResourcesJoinModel", lazy="select", foreign_keys="UsersResourcesJoinModel.user_id")

    def to_dict(self):
        return {
            "name": self.name,
            "surname": self.surname,
            "role": self.role,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "company": self.company.to_dict() if self.company else None,
            "resources": [r.to_dict() for r in self.resources]
        }