import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    report_directory: Path
    database_path: Path
    request_timeout: int = 20
    max_results: int = 5
    max_page_characters: int = 12000


def get_settings() -> Settings:
    return Settings(
        report_directory=Path(
            os.getenv("REPORT_DIRECTORY", str(PROJECT_ROOT / "reports"))
        ),
        database_path=Path(
            os.getenv(
                "DATABASE_PATH",
                str(PROJECT_ROOT / "storage" / "researchpilot.sqlite3"),
            )
        ),
        request_timeout=int(os.getenv("REQUEST_TIMEOUT", "20")),
        max_results=int(os.getenv("MAX_RESULTS", "5")),
        max_page_characters=int(os.getenv("MAX_PAGE_CHARACTERS", "12000")),
    )
