import os
import yaml
import streamlit as st

# Correct MCP config path
MCP_PATH = os.path.join("src", "preppilot", "mcp", "context_config.yaml")

# Load MCP config
def load_mcp():
    if not os.path.exists(MCP_PATH):
        return {}
    with open(MCP_PATH, "r") as f:
        return yaml.safe_load(f) or {}

# Save MCP config
def save_mcp(data):
    with open(MCP_PATH, "w") as f:
        yaml.dump(data, f, sort_keys=False)

# Streamlit UI
def main():
    st.set_page_config(page_title="🧠 MCP Editor", layout="centered")
    st.title("🧠 Model Context Protocol Editor")
    st.caption("Easily manage agent prompts & model settings")

    config = load_mcp()

    if not config:
        st.warning("No agents found in MCP config.")
        return

    agent_ids = list(config.keys())
    selected_agent = st.selectbox("🧠 Select an Agent", agent_ids)
    st.markdown("---")

    # Show editable model and prompt
    current_model = config[selected_agent].get("model", "")
    current_prompt = config[selected_agent].get("prompt", "")

    new_model = st.text_input("🔧 Model Name", value=current_model)
    new_prompt = st.text_area("✏️ Prompt Template", value=current_prompt, height=300)

    if st.button("💾 Save Changes"):
        config[selected_agent]["model"] = new_model
        config[selected_agent]["prompt"] = new_prompt
        save_mcp(config)
        st.success("✅ Agent updated successfully!")

    st.markdown("---")
    st.subheader("📁 Raw Config Preview")
    st.code(yaml.dump(config, sort_keys=False), language="yaml")

if __name__ == "__main__":
    main()
