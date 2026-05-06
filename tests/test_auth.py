from src.auth.service import AuthService
from src.auth.store import AuthStore
from src.storage.metadata_db import MetadataDB


def test_register_and_login(tmp_path):
    db = MetadataDB(str(tmp_path / "metadata.db"))
    service = AuthService(AuthStore(db))
    service.register("user@example.com", "password123")
    user = service.login("user@example.com", "password123")
    assert user["email"] == "user@example.com"


def test_invalid_password_rejected(tmp_path):
    db = MetadataDB(str(tmp_path / "metadata.db"))
    service = AuthService(AuthStore(db))
    service.register("user@example.com", "password123")
    try:
        service.login("user@example.com", "wrongpass")
        assert False
    except ValueError:
        assert True
