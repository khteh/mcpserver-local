from mcpserver.main import add_numbers, echo, greet, help_text, system_info


def test_greet_returns_expected_message() -> None:
    assert greet("Ada") == "Hello, Ada!"


def test_echo_returns_input_message() -> None:
    assert echo("MCP") == "MCP"


def test_add_numbers_returns_sum() -> None:
    assert add_numbers(2, 3) == 5


def test_system_info_returns_runtime_data() -> None:
    info = system_info()

    assert isinstance(info, dict)
    assert "os" in info
    assert "python_version" in info


def test_help_text_references_tool_names() -> None:
    text = help_text()

    assert "greet(name)" in text
    assert "system_info()" in text
