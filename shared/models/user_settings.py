from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from shared.models.aygit_base import AygitBaseModel

class UserSettingsModel(AygitBaseModel):
    __tablename__ = 'user_settings'

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("AygitUserModel", lazy="joined")


    email_notifications = Column(JSONB, nullable=False)
    mobile_notifications = Column(JSONB, nullable=False)
    language = Column(String, nullable=False)

    def to_dict(self):
        return {
            "email_notifications": self.email_notifications,
            "mobile_notifications": self.mobile_notifications,
            "language": self.language
        }