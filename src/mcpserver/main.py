import argparse, json, logging, sys
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from html import parser
from platform import machine, python_version, system
from sys import argv
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("mcpserver-local")

PROMPT_TEMPLATE = (
    "You are a local mcpserver, a simple MCP application. "
    "Available tools: greet(name), echo(message), add_numbers(a, b), "
    "system_info(), help_text()."
)
parser = argparse.ArgumentParser(description='A simple local MCP server application.')
parser.add_argument('-g', '--greet', nargs='?', const='World', default='World')
parser.add_argument('-e', '--echo', nargs='?', const='', default='')
parser.add_argument('-a', '--add-numbers', nargs=2, type=int, default=(0, 0))
parser.add_argument('-i', '--system-info', action='store_true', help="Display system information")
parser.add_argument('-h', '--help', action='store_true', help="Display help information")

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """
    Copilot cannot pass CLI arguments directly to your script through a chat prompt because MCP tools expose functions, not terminal commands [1].
    When you use the standard FastMCP framework, the mcp.json file starts your python process once using standard input/output (stdio) [1]. 
    Copilot can only invoke Python functions that you explicitly declare as tools using decorators [1]. It completely bypasses your argparse CLI block after the server starts.
    To pass your parameters through the prompt without breaking your existing codebase, you need to add an MCP function wrapper that feeds your parameters directly into your existing argparse logic.    
    """
    return parser.parse_args(argv)

def configure_logging(log_path: str | Path | None = None) -> None:
    """Configure the root logger and ensure the log directory exists."""
    log_file = Path(log_path) if log_path is not None else Path("/var/log/mcpserver-local/mcpserver.log")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler = TimedRotatingFileHandler(log_file, when="midnight", backupCount=3)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

@mcp.tool()
def greet(name: str) -> str:
    """
    Executes the greet command with CLI parameters.
    Pass arguments exactly as you would on the command line, like '--greet Alex'.
    """
    # Split the prompt's string parameter into a list just like sys.argv
    parsed_args = parse_args(name.split())
    return f"Hello, {parsed_args.greet}!"

@mcp.tool()
def echo(message: str) -> str:
    """
    Executes the echo command with CLI parameters.
    Pass arguments exactly as you would on the command line, like '--echo "What's up?"'.
        """
    parsed_args = parse_args(message.split())
    return parsed_args.echo


@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """
    Executes the add_numbers command with CLI parameters.
    Pass arguments exactly as you would on the command line, like '--add-numbers 5 10'.
    """
    parsed_args = parse_args(['-a', str(a), str(b)])
    return parsed_args.add_numbers[0] + parsed_args.add_numbers[1]


@mcp.tool()
def system_info(args:str) -> dict:
    """
    Executes the system_info command with CLI parameters.
    Pass arguments exactly as you would on the command line, like '--system-info'.

    Return information about the current runtime environment.
    """
    parsed_args = parse_args(args.split())
    return {
        "os": system(),
        "machine": machine(),
        "python_version": python_version(),
    } if parsed_args.system_info else {}

@mcp.tool()
def help_text(args:str) -> str:
    """
    Executes the help_text command with CLI parameters.
    Pass arguments exactly as you would on the command line, like '--help'.

    Return usage guidance and the server prompt template.
    """
    # Get standard CLI text block as a string
    raw_help_text = parser.format_help()

    # Package it cleanly into a JSON object
    return json.dumps({"mcpserver-local-help": raw_help_text}, indent=4)

def main() -> None:
    mcp.run(transport="stdio")
