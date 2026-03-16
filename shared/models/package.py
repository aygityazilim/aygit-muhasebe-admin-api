from shared.models.aygit_base import AygitBaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class PackageModel(AygitBaseModel):
    __tablename__ = "packages"

    key = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    resources = relationship("PackagesResourcesJoinModel", lazy="select", foreign_keys="PackagesResourcesJoinModel.package_id")

    def to_dict(self):
        return {
            "id": self.id,
            "key": self.key,
            "name": self.name,
            "description": self.description,
            "resources": [r.to_dict() for r in self.resources]
        }
