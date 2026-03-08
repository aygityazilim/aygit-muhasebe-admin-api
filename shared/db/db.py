from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from shared.config import Config

admin_engine = create_engine(
    Config.ADMIN_DATABASE_URL,
    pool_pre_ping=True
)

registiration_engine = create_engine(
    Config.REGISTIRATION_DATABASE_URL,
    pool_pre_ping=True
)

AdminSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=admin_engine)
RegistirationSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=registiration_engine)

AdminBase = declarative_base()
RegistirationBase = declarative_base()

def get_admin_db():
    db = AdminSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_registiration_db():
    db = RegistirationSessionLocal()
    try:
        yield db
    finally:
        db.close()
