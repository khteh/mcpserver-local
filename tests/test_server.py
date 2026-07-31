import logging
from mcpserver.main import add_numbers, echo, fibonacci, greet, system_info
from pathlib import Path
from src.mcpserver.main import configure_logging

def test_greet_returns_expected_message() -> None:
    assert greet("Ada") == "Hello, Ada!"

def test_greet_handles_quoted_name() -> None:
    assert greet('-g "Mickey Mouse"') == "Hello, Mickey Mouse!"


def test_echo_returns_input_message() -> None:
    assert echo("MCP") == "MCP"


def test_add_numbers_returns_sum() -> None:
    assert add_numbers(2, 3) == 5


def test_fibonacci_parses_cli_style_input() -> None:
    assert fibonacci('-f 25') == 75025


def test_system_info_returns_runtime_data() -> None:
    info = system_info()

    assert isinstance(info, dict)
    assert "os" in info
    assert "python_version" in info


def test_configure_logging_creates_missing_directory(tmp_path: Path) -> None:
    log_path = tmp_path / "nested" / "mcpserver.log"

    configure_logging(log_path)

    assert log_path.parent.exists()
    assert any(isinstance(handler, logging.Handler) for handler in logging.getLogger().handlers)
