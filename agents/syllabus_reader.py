import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("MODEL", "gemini-1.5-flash")


class SyllabusReaderAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(MODEL)

    def extract_topics(self, raw_syllabus_text: str):
        prompt = f"""
You are an academic assistant.

Given the following syllabus, extract a structured list of chapters and topics.

Format:
[
  {{
    "chapter": "Chapter Title",
    "topics": ["Topic 1", "Topic 2"]
  }}
]

ONLY return JSON. Do NOT include markdown or backticks.

Syllabus:
\"\"\"
{raw_syllabus_text}
\"\"\"
"""

        try:
            response = self.model.generate_content(prompt)
            output = response.text.strip()
            print("\n[DEBUG] Gemini Raw Output:\n", output)

            # ✅ Clean output if Gemini wrapped it with ```
            if output.startswith("```json") or output.startswith("```"):
                output = output.strip("`").replace("json", "").strip()

            return json.loads(output)

        except Exception as e:
            print(f"[SyllabusReaderAgent] Error: {e}")
            return []
