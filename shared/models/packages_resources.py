from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from shared.models.aygit_base import AygitBaseModel

class PackagesResourcesJoinModel(AygitBaseModel):
    __tablename__ = "packages_resources"

    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    resource = relationship("ResourceModel", lazy="select")

    package_id = Column(Integer, ForeignKey("packages.id"), nullable=False)
    package = relationship("PackageModel", lazy="select")

    def to_dict(self):
        return self.resource.to_dict()