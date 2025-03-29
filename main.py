from tasks.study_flow import StudyFlow

# Sample syllabus input (can be replaced with file/CV upload later)
sample_syllabus = """
Week 1: Introduction to Artificial Intelligence
- History of AI
- Applications of AI

Week 2: Machine Learning Basics
- Supervised Learning
- Unsupervised Learning
"""

if __name__ == "__main__":
    study_flow = StudyFlow()
    results = study_flow.run(sample_syllabus)
