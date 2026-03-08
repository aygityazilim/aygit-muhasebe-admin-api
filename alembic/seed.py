import os
import sys
from dotenv import load_dotenv
import hashlib

base_dir = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, ".env"))
sys.path.append(base_dir)

from shared.db.db import AdminSessionLocal
from shared.models.user import UserModel


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def seed_admin_user():
    db = AdminSessionLocal()
    try:
        existing = db.query(UserModel).filter(UserModel.email == "admin@admin.com").first()
        if existing:
            print("Admin user already exists, skipping.")
            return

        admin = UserModel(
            email="admin@admin.com",
            password=hash_password("123123"),
            name="Admin",
            surname="Admin",
        )
        db.add(admin)
        db.commit()
        print("Admin user created successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin_user()
