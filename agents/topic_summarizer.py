import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("MODEL", "gemini-1.5-flash")


class TopicSummarizerAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(MODEL)

    def summarize_topics(self, structured_syllabus: list) -> dict:
        """
        Input:
        [
          {
            "chapter": "Machine Learning Basics",
            "topics": ["Supervised Learning", "Unsupervised Learning"]
          }
        ]

        Output:
        {
          "Machine Learning Basics": {
            "Supervised Learning": ["• Summary 1", "• Summary 2"],
            "Unsupervised Learning": ["• Summary 1", "• Summary 2"]
          }
        }
        """
        prompt = f"""
You are an intelligent summarizer.

For each chapter and topic in the following syllabus, write 2-3 bullet-point summaries per topic.

Format:
{{
  "Chapter Title": {{
    "Topic Name": [
      "Bullet point 1",
      "Bullet point 2"
    ]
  }}
}}

ONLY return valid JSON. No extra text or markdown.

Syllabus:
{structured_syllabus}
"""

        try:
            response = self.model.generate_content(prompt)
            output = response.text.strip()
            print("\n[DEBUG] Gemini Raw Output (Summarizer):\n", output)

            if output.startswith("```json") or output.startswith("```"):
                output = output.strip("`").replace("json", "").strip()

            return json.loads(output)

        except Exception as e:
            print(f"[TopicSummarizerAgent] Error: {e}")
            return {}
