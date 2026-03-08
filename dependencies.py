from fastapi import Depends
from sqlalchemy.orm import Session
from shared.db import get_admin_db
from services.auth import AuthService

def get_auth_service(db: Session = Depends(get_admin_db)) -> AuthService:
    return AuthService(db=db)