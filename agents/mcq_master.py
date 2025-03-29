import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("MODEL", "gemini-1.5-flash")


class MCQMasterAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(MODEL)

    def generate_mcqs(self, structured_syllabus: list) -> dict:
        """
        Input:
        [
          {
            "chapter": "Intro to AI",
            "topics": ["History of AI", "Applications of AI"]
          }
        ]

        Output:
        {
          "Intro to AI": {
            "History of AI": [
              {
                "question": "...",
                "options": ["A", "B", "C", "D"],
                "answer": "B"
              }
            ]
          }
        }
        """
        prompt = f"""
You are a professional MCQ setter.

For each topic below, create 3-4 multiple-choice questions with 4 options each and the correct answer.

Format:
{{
  "Chapter Title": {{
    "Topic Name": [
      {{
        "question": "...",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "answer": "A"
      }}
    ]
  }}
}}

ONLY return valid JSON. Do not include any explanation or markdown.

Syllabus:
{structured_syllabus}
"""

        try:
            response = self.model.generate_content(prompt)
            output = response.text.strip()
            print("\n[DEBUG] Gemini Raw Output (MCQs):\n", output)

            if output.startswith("```json") or output.startswith("```"):
                output = output.strip("`").replace("json", "").strip()

            return json.loads(output)

        except Exception as e:
            print(f"[MCQMasterAgent] Error: {e}")
            return {}
