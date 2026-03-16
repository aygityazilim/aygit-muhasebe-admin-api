from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from shared.models.aygit_base import AygitBaseModel

class ResourceModel(AygitBaseModel):
    __tablename__ = "resources"
    key = Column(String, nullable=False)
    sort_order = Column(Integer, nullable=False, default=0)
    is_menu = Column(Boolean, nullable=False, default=False)
    path = Column(String, nullable=True)

    parent_id = Column(Integer, ForeignKey("resources.id"), nullable=True)
    parent = relationship("ResourceModel", lazy="select")

    def to_dict(self):
        return {
            "id": self.id,
            "key": self.key,
            "sort_order": self.sort_order,
            "is_menu": self.is_menu,
            "path": self.path,
            "parent_id": self.parent_id,
        }
