# File: tests/test_mcp_protocol.py

import os
import pytest
yaml = __import__('yaml')

from src.preppilot.mcp.protocol import load_agent_context, inject_variables

# Create a temporary MCP config for testing
TEST_MCP_PATH = "tests/test_context_config.yaml"

TEST_CONFIG = {
    "dummy_agent": {
        "model": "gemini-test",
        "prompt": "Hello, {name}! You are studying {subject}."
    }
}

@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    os.makedirs("tests", exist_ok=True)
    with open(TEST_MCP_PATH, "w") as f:
        yaml.dump(TEST_CONFIG, f)
    yield
    os.remove(TEST_MCP_PATH)


def test_load_agent_context_valid():
    os.environ["MCP_PATH"] = TEST_MCP_PATH
    ctx = load_agent_context("dummy_agent")
    assert ctx["model"] == "gemini-test"
    assert "{name}" in ctx["prompt"]


def test_load_agent_context_invalid():
    os.environ["MCP_PATH"] = TEST_MCP_PATH
    with pytest.raises(ValueError):
        load_agent_context("nonexistent")


def test_inject_variables_success():
    prompt = "Welcome, {name}, to {place}."
    values = {"name": "Fahad", "place": "PrepPilot"}
    filled = inject_variables(prompt, values)
    assert filled == "Welcome, Fahad, to PrepPilot."


def test_inject_variables_missing():
    prompt = "Hi {name}, welcome to {place}."
    values = {"name": "Fahad"}  # missing 'place'
    with pytest.raises(ValueError):
        inject_variables(prompt, values)
