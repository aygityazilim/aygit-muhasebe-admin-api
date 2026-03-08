from fastapi import HTTPException
from sqlalchemy.orm import Session
from shared.repositories import UserRepository
from shared.schemas import (
    LoginSchema
)
from shared.enums import (
    StatusCodeEnum,
    ErrorMessageEnum
)
from shared.utils import PasswordUtil
from shared.config import Config
import jwt

class AuthService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db=db)

    async def login(self, payload: LoginSchema) -> str:
        try:
            user = self.user_repository.get_by_field("email", payload.email)
            if PasswordUtil.hash(payload.password) != user.password:
                raise HTTPException(status_code=StatusCodeEnum.NOT_FOUND.value, detail=ErrorMessageEnum.USER_NOT_FOUND.value)            
            data = jwt.encode({"name": user.name, "surname": user.surname, "email": user.email}, Config.JWT_SECRET, algorithm="HS256")
            return data
        except HTTPException:
            raise
        except Exception as e:
            print(e)
            raise e
