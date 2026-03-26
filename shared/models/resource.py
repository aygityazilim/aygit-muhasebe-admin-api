from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from shared.models.aygit_base import AygitBaseModel

class ResourceModel(AygitBaseModel):
    __tablename__ = "resources"
    key = Column(String, nullable=False)        
    path = Column(String, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "key": self.key,                                                
        }
