# Local MCP Server

This project is a small Python MCP server implemented with `mcp` and managed with `uv`. It is bootstrapped / created entirely using Copilot agent with mcp-server-dev SKILLS.

## Launch the server

From the repository root:

```bash
cd <project folder>
uv run mcpserver-local
```

This starts the MCP server using the default MCP transport, which is the stdio transport.

## Quick local test

A simple CLI helper is available for manual testing:

```bash
uv run mcpserver-local-cli greet Ada
uv run mcpserver-local-cli add_numbers 2 3
uv run mcpserver-local-cli system_info
uv run mcpserver-local-cli help
```

## How a client / agent connects

The server is designed for local process-based connection via stdin/stdout. A client or agent can spawn `uv run mcpserver-local` and exchange MCP messages over the process pipes.

### Local client pattern

A typical client uses a subprocess to launch the server and then sends/receives MCP frames on stdin/stdout.

Example pseudo-code:

```python
import subprocess

proc = subprocess.Popen(
    ["uv", "run", "mcpserver-local"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

# exchange MCP JSON/RPC frames with proc.stdin / proc.stdout
# depending on the MCP client implementation
```

## Notes

- `mcpserver-local-cli` is a convenience tool for local testing, not a transport endpoint for external MCP clients.
- If you need network access later, the server can be extended with a transport that supports TCP or websockets.
