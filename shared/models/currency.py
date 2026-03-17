from sqlalchemy import Column, String, JSON
from shared.models.aygit_base import AygitBaseModel

class CurrencyModel(AygitBaseModel):
    __tablename__ = "currencies"

    code = Column(String, unique=True, nullable=False)
    name = Column(JSON, nullable=False)    
    symbol = Column(String, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "symbol": self.symbol
        }