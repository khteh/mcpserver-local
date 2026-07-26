from mcpserver.cli import main


def test_cli_greet_returns_message(capsys):
    assert main(["greet", "Ada"]) == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello, Ada!"


def test_cli_add_numbers_returns_sum(capsys):
    assert main(["add_numbers", "2", "3"]) == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "5"


def test_cli_system_info_returns_json(capsys):
    assert main(["system_info"]) == 0
    captured = capsys.readouterr()
    assert "python_version" in captured.out


def test_cli_help_returns_text(capsys):
    assert main(["help"]) == 0
    captured = capsys.readouterr()
    assert "Available tools" in captured.out
