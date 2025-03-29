import os
import yaml

# Path to your MCP YAML configuration
MCP_PATH = os.path.join("src", "preppilot", "mcp", "context_config.yaml")

def load_agent_context(agent_id: str) -> dict:
    """
    Load the model and prompt context for a specific agent ID from the MCP config.
    """
    if not os.path.exists(MCP_PATH):
        raise FileNotFoundError(f"❌ MCP file not found at {MCP_PATH}")

    with open(MCP_PATH, "r") as f:
        config = yaml.safe_load(f) or {}

    if agent_id not in config:
        raise ValueError(f"❌ No context found for agent: {agent_id}")

    return config[agent_id]

def inject_variables(template: str, variables: dict) -> str:
    for key, value in variables.items():
        template = template.replace(f"{{{{{key}}}}}", str(value))
    return template


def get_model_name(agent_id: str) -> str:
    """
    Return just the model name for the given agent (fallback = gemini-1.5-flash)
    """
    context = load_agent_context(agent_id)
    return context.get("model", "gemini-1.5-flash")


def build_prompt(agent_id: str, input_data: str) -> str:
    """
    Return the final prompt by injecting input into the agent's prompt template.
    """
    context = load_agent_context(agent_id)
    template = context.get("prompt", "")
    return template.replace("{input}", input_data.strip())
