from __future__ import annotations

from src.storage.metadata_db import MetadataDB


class AuthStore:
    def __init__(self, metadata_db: MetadataDB) -> None:
        self.metadata_db = metadata_db

    def create_user(self, email: str, password_hash: str) -> str:
        return self.metadata_db.create_user(email=email, password_hash=password_hash)

    def get_user_by_email(self, email: str):
        return self.metadata_db.get_user_by_email(email=email)
