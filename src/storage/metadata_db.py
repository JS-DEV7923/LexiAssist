from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any


class MetadataDB:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    path TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS chats (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    citations_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

    def create_user(self, email: str, password_hash: str) -> str:
        user_id = str(uuid.uuid4())
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO users (id, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                (user_id, email, password_hash, datetime.utcnow().isoformat()),
            )
        return user_id

    def get_user_by_email(self, email: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            return dict(row) if row else None

    def add_document(self, user_id: str, name: str, path: str) -> str:
        doc_id = str(uuid.uuid4())
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO documents (id, user_id, name, path, created_at) VALUES (?, ?, ?, ?, ?)",
                (doc_id, user_id, name, path, datetime.utcnow().isoformat()),
            )
        return doc_id

    def list_documents(self, user_id: str) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM documents WHERE user_id = ? ORDER BY created_at DESC", (user_id,)
            ).fetchall()
            return [dict(r) for r in rows]

    def get_document(self, user_id: str, doc_id: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM documents WHERE id = ? AND user_id = ?", (doc_id, user_id)
            ).fetchone()
            return dict(row) if row else None

    def delete_document(self, user_id: str, doc_id: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM documents WHERE id = ? AND user_id = ?", (doc_id, user_id))

    def add_chat(self, user_id: str, question: str, answer: str, citations_json: str) -> str:
        chat_id = str(uuid.uuid4())
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO chats (id, user_id, question, answer, citations_json, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (chat_id, user_id, question, answer, citations_json, datetime.utcnow().isoformat()),
            )
        return chat_id

    def list_chats(self, user_id: str, limit: int = 50) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM chats WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
                (user_id, limit),
            ).fetchall()
            return [dict(r) for r in rows]
