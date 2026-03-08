from sqlalchemy import Column, String
from shared.models.base import BaseModel

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