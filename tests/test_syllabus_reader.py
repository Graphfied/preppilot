import os
from agents.syllabus_reader import SyllabusReaderAgent

# Load environment variables from the .env file
from dotenv import load_dotenv
load_dotenv()

# Sample syllabus text
syllabus_text = """
Week 1: Introduction to Artificial Intelligence
- History of AI
- Applications of AI

Week 2: Machine Learning Basics
- Supervised Learning
- Unsupervised Learning
"""

# Initialize the agent
syllabus_reader = SyllabusReaderAgent()

# Extract topics
structured_topics = syllabus_reader.extract_topics(syllabus_text)
print(structured_topics)
