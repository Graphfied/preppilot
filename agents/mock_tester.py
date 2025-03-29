import os
import json
import random
try:
    from src.preppilot.mcp.protocol import load_agent_context
except ImportError:
    def load_agent_context(agent_name: str):
        print(f"[Warning] Using fallback for load_agent_context. Agent: {agent_name}")
        return {"instructions": "Default instructions."}

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

class MockTesterAgent:
    def __init__(self):
        self.context = load_agent_context("mock_tester")

    def conduct_mock_exam(self, mcqs: dict, num_questions: int = 5) -> dict:
        all_questions = []

        for chapter, topics in mcqs.items():
            for topic, questions in topics.items():
                for q in questions:
                    all_questions.append({
                        "chapter": chapter,
                        "topic": topic,
                        "question": q["question"],
                        "options": q["options"],
                        "answer": q["answer"]
                    })

        if not all_questions:
            print("[MockTesterAgent] No MCQs available for testing.")
            return {"questions": [], "total": 0}

        selected = random.sample(all_questions, min(num_questions, len(all_questions)))

        exam_data = {
            "questions": selected,
            "total": len(selected),
            "instructions": self.context.get("instructions", "Answer each question.")
        }

        output_path = os.path.join(RESULTS_DIR, "mock_exam.json")
        with open(output_path, "w") as f:
            json.dump(exam_data, f, indent=2)

        print(f"\n📝 Mock exam saved to {output_path} — ready for user to answer.")
        return exam_data
