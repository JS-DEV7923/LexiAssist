from __future__ import annotations

from passlib.context import CryptContext

from src.auth.store import AuthStore


class AuthService:
    def __init__(self, store: AuthStore) -> None:
        self.store = store
        self._pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

    def register(self, email: str, password: str) -> str:
        email = email.strip().lower()
        if "@" not in email:
            raise ValueError("Invalid email")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        existing = self.store.get_user_by_email(email)
        if existing:
            raise ValueError("User already exists")
        password_hash = self._pwd_context.hash(password)
        return self.store.create_user(email=email, password_hash=password_hash)

    def login(self, email: str, password: str) -> dict:
        email = email.strip().lower()
        user = self.store.get_user_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")
        if not self._pwd_context.verify(password, user["password_hash"]):
            raise ValueError("Invalid credentials")
        return {"id": user["id"], "email": user["email"]}
