from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from shared.models.aygit_base import AygitBaseModel

class UsersResourcesJoinModel(AygitBaseModel):
    __tablename__ = "users_resources"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("AygitUserModel", lazy="select")

    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    resource = relationship("ResourceModel", lazy="select")

    def to_dict(self):
        return self.resource.to_dict()
