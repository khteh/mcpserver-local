import os
import pytest

def pytest_configure(config):
    # Detects the custom MCP flag and immediately short-circuits the test runner
    if os.getenv("SKIP_PYTEST_ON_MCP") == "true":
        print("MCP Session detected: Bypassing pytest runner initialization.")
        pytest.exit("Skipping tests for active MCP server session.")
