import sqlite3
from datetime import datetime
from pathlib import Path

from agent.researcher import ResearchSource


class ResearchDatabase:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS research_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    report_path TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER NOT NULL REFERENCES research_runs(id),
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    content TEXT NOT NULL,
                    read_error TEXT
                );
                """
            )

    def save_run(
        self,
        question: str,
        report_path: Path,
        sources: list[ResearchSource],
        created_at: datetime,
    ) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO research_runs (question, report_path, created_at) "
                "VALUES (?, ?, ?)",
                (question, str(report_path), created_at.isoformat()),
            )
            run_id = int(cursor.lastrowid)
            connection.executemany(
                "INSERT INTO sources (run_id, title, url, content, read_error) "
                "VALUES (?, ?, ?, ?, ?)",
                [
                    (
                        run_id,
                        source.title,
                        source.url,
                        source.content,
                        source.read_error,
                    )
                    for source in sources
                ],
            )
        return run_id

    def list_runs(self, limit: int = 10) -> list[sqlite3.Row]:
        if limit < 1:
            raise ValueError("limit must be at least 1.")
        with self._connect() as connection:
            return connection.execute(
                "SELECT id, question, report_path, created_at "
                "FROM research_runs ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
