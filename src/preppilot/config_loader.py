import os
import sys

# 🔥 Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from agents.syllabus_reader import SyllabusReaderAgent
from agents.topic_summarizer import TopicSummarizerAgent
from agents.mcq_master import MCQMasterAgent
from agents.mock_tester import MockTesterAgent
import yaml
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
# Check if the environment variable is set
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in your .env file.")
# Check if the environment variable is set
MODEL = os.getenv("MODEL", "gemini/gemini-1.5-flash")
if not MODEL:
    raise ValueError("MODEL is missing in your .env file.")
# Check if the environment variable is set


AGENT_CLASSES = {
    "syllabus_reader": SyllabusReaderAgent,
    "topic_summarizer": TopicSummarizerAgent,
    "mcq_master": MCQMasterAgent,
    "mock_tester": MockTesterAgent
}

def load_yaml(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def load_agents(agent_config_path: str):
    data = load_yaml(agent_config_path)
    agents = {}
    for agent_id, details in data.items():
        agent_class = AGENT_CLASSES.get(agent_id)
        if not agent_class:
            raise ValueError(f"No class found for agent id: {agent_id}")
        agents[agent_id] = agent_class()
    return agents

def load_tasks(task_config_path: str, agents: dict):
    data = load_yaml(task_config_path)
    tasks = []

    for task_id, task_info in data.items():
        agent_id = task_info['agent']
        if agent_id not in agents:
            raise ValueError(f"Agent '{agent_id}' not found for task '{task_id}'")

        tasks.append({
            "id": task_id,
            "description": task_info['description'],
            "expected_output": task_info['expected_output'],
            "agent": agents[agent_id]
        })

    return tasks
