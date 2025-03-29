# agents/mcq_master.py

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from src.preppilot.mcp.protocol import load_agent_context, inject_variables

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class MCQMasterAgent:
    def __init__(self):
        config = load_agent_context("mcq_master")
        self.model_name = config["model"]
        self.prompt_template = config["prompt"]
        self.model = genai.GenerativeModel(self.model_name)

    def generate_mcqs(self, structured: list) -> dict:
        prompt = inject_variables(self.prompt_template, {"input": structured})
        try:
            response = self.model.generate_content(prompt)
            output = response.text.strip()
            if output.startswith("```"): output = output.strip("`").replace("json", "").strip()
            return json.loads(output)
        except Exception as e:
            print(f"[MCQMasterAgent] Error: {e}")
            return {}
