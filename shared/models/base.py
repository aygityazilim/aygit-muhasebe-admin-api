from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, Boolean, DateTime
from shared.db.db import AdminBase

class BaseModel(AdminBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())