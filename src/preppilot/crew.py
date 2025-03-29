import os
from config_loader import load_agents, load_tasks


# Paths to config files
AGENTS_PATH = "src/preppilot/config/agents.yaml"
TASKS_PATH = "src/preppilot/config/tasks.yaml"

# Sample syllabus input for testing
raw_syllabus = """
Week 1: Introduction to Artificial Intelligence
- History of AI
- Applications of AI

Week 2: Machine Learning Basics
- Supervised Learning
- Unsupervised Learning
"""

def run():
    print("\n⚙️  Loading agents and tasks from YAML...")
    agents = load_agents(AGENTS_PATH)
    tasks = load_tasks(TASKS_PATH, agents)

    context = {}

    for task in tasks:
        print(f"\n🚀 Task: {task['id']} - {task['description']}")

        # Task execution flow based on task id
        if task['id'] == "study_pipeline":
            output = task['agent'].extract_topics(raw_syllabus)

        elif task['id'] == "summarize_topics":
            syllabus_data = context.get('study_pipeline')
            output = task['agent'].summarize_topics(syllabus_data)

        elif task['id'] == "generate_mcqs":
            syllabus_data = context.get('study_pipeline')
            output = task['agent'].generate_mcqs(syllabus_data)

        elif task['id'] == "mock_exam":
            mcqs = context.get('generate_mcqs')
            output = task['agent'].conduct_mock_exam(mcqs)

        else:
            output = None

        context[task['id']] = output
        print(f"✅ Output for {task['id']}:\n{output}")

    print("\n📊 Final Exam Ready!")
    print("Go to: results/mock_exam.json to take your test ✅")


if __name__ == "__main__":
    run()