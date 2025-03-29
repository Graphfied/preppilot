import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(os.getenv("MODEL", "gemini-1.5-flash"))
response = model.generate_content("Write 3 points about Artificial Intelligence.")
print(response.text)
