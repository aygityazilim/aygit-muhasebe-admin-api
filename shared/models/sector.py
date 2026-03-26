from sqlalchemy import Column, String, JSON
from shared.models.aygit_base import AygitBaseModel

class SectorModel(AygitBaseModel):
    __tablename__ = "sectors"

    name = Column(JSON, nullable=False)
    description = Column(String, nullable=True)
    slug = Column(String, nullable=False)

    def to_dict(self): 
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "slug": self.slug
        }