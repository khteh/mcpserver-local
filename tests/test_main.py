from pathlib import Path

import logging

from src.main import configure_logging


def test_configure_logging_creates_missing_directory(tmp_path: Path) -> None:
    log_path = tmp_path / "nested" / "mcpserver.log"

    configure_logging(log_path)

    assert log_path.parent.exists()
    assert any(isinstance(handler, logging.Handler) for handler in logging.getLogger().handlers)
