from platform import machine, python_version, system

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcpserver-local")

PROMPT_TEMPLATE = (
    "You are a local mcpserver, a simple MCP application. "
    "Available tools: greet(name), echo(message), add_numbers(a, b), "
    "system_info(), help_text()."
)


@mcp.tool()
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"


@mcp.tool()
def echo(message: str) -> str:
    """Return the provided message verbatim."""
    return message


@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two integers together."""
    return a + b


@mcp.tool()
def system_info() -> dict:
    """Return information about the current runtime environment."""
    return {
        "os": system(),
        "machine": machine(),
        "python_version": python_version(),
    }


@mcp.tool()
def help_text() -> str:
    """Return usage guidance and the server prompt template."""
    return (
        "Available tools: greet(name), echo(message), add_numbers(a, b), "
        "system_info(), help_text(). "
        f"Prompt template: {PROMPT_TEMPLATE}"
    )


def main() -> None:
    mcp.run()
