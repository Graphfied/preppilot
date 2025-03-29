from agents.syllabus_reader import SyllabusReaderAgent
from agents.topic_summarizer import TopicSummarizerAgent
from agents.mcq_master import MCQMasterAgent
from agents.mock_tester import MockTesterAgent

class StudyFlow:
    def __init__(self):
        self.syllabus_reader = SyllabusReaderAgent()
        self.topic_summarizer = TopicSummarizerAgent()
        self.mcq_master = MCQMasterAgent()
        self.mock_tester = MockTesterAgent()

    def run(self, raw_syllabus_text: str):
        print("\n🚀 Step 1: Reading Syllabus...")
        structured_syllabus = self.syllabus_reader.extract_topics(raw_syllabus_text)
        print(f"✅ Extracted Topics:\n{structured_syllabus}")

        print("\n🧠 Step 2: Summarizing Topics...")
        summaries = self.topic_summarizer.summarize_topics(structured_syllabus)
        print(f"📋 Bullet Notes:\n{summaries}")

        print("\n📚 Step 3: Generating MCQs...")
        mcqs = self.mcq_master.generate_mcqs(structured_syllabus)
        print(f"❓ MCQ Bank:\n{mcqs}")

        print("\n🎯 Step 4: Running Mock Test...")
        result = self.mock_tester.conduct_mock_exam(mcqs)

        print("\n📊 Final Score:")
        print(f"You scored {result['score']} out of {result['total']}")

        return {
            "topics": structured_syllabus,
            "summaries": summaries,
            "mcqs": mcqs,
            "mock_result": result
        }
