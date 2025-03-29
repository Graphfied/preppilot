import os
import sys
import json
import fitz  # PyMuPDF
import streamlit as st
from uuid import uuid4
from datetime import datetime

# Add root directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.syllabus_reader import SyllabusReaderAgent
from agents.topic_summarizer import TopicSummarizerAgent
from agents.mcq_master import MCQMasterAgent

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        return "".join([page.get_text() for page in doc])

def save_data(session_id, syllabus, topics, summaries, mcqs):
    data = {
        "syllabus": syllabus,
        "structured_topics": topics,
        "summaries": summaries,
        "mcqs": mcqs
    }
    path = os.path.join(RESULTS_DIR, f"{session_id}_pipeline.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path

def run_agents(syllabus_text):
    reader = SyllabusReaderAgent()
    summarizer = TopicSummarizerAgent()
    mcq_maker = MCQMasterAgent()

    topics = reader.extract_topics(syllabus_text)
    summaries = summarizer.summarize_topics(topics)
    mcqs = mcq_maker.generate_mcqs(topics)
    return topics, summaries, mcqs

def main():
    st.set_page_config(page_title="PrepPilot AI", layout="centered")
    st.title("📚 PrepPilot AI Study Assistant")
    st.caption("Smart study guide, powered by AI 🚀")

    # --- LOGIN ---
    if "logged_in" not in st.session_state:
        with st.form("login_form"):
            name = st.text_input("👤 Your Name")
            email = st.text_input("📧 Your Email")
            submitted = st.form_submit_button("Continue")
        if submitted and name and email:
            st.session_state["logged_in"] = True
            st.session_state["name"] = name
            st.session_state["email"] = email
            st.rerun()
        else:
            st.stop()

    name = st.session_state["name"]
    email = st.session_state["email"]
    session_id = f"{name}_{str(uuid4())[:6]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Ensure exam state
    if "start_exam" not in st.session_state:
        st.session_state["start_exam"] = False

    st.success(f"Welcome {name}! Let's get started 🔥")
    st.markdown("---")

    # --- SYLLABUS INPUT ---
    st.subheader("📥 Upload your syllabus")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    text_input = st.text_area("Or paste your syllabus here:")

    syllabus_text = ""
    if uploaded_file:
        syllabus_text = extract_text_from_pdf(uploaded_file)
        st.success("✅ PDF uploaded and text extracted.")
    elif text_input.strip():
        syllabus_text = text_input.strip()
        st.success("✅ Text captured.")

    # --- RUN AGENTS ---
    if syllabus_text and not st.session_state["start_exam"]:
        st.markdown("Click below to run the AI agents on your syllabus.")
        if st.button("🤖 Run AI Agents"):
            with st.spinner("Running agents..."):
                topics, summaries, mcqs = run_agents(syllabus_text)
                save_data(session_id, syllabus_text, topics, summaries, mcqs)

            # Save results to session state
            st.session_state["exam_data"] = {
                "session_id": session_id,
                "mcqs": mcqs,
                "name": name,
                "email": email
            }
            st.session_state["topics"] = topics
            st.session_state["summaries"] = summaries
            st.session_state["mcqs"] = mcqs

    if "exam_data" in st.session_state and not st.session_state["start_exam"]:
        st.success("✅ Done! Here's your personalized study material:")

        st.markdown("### 📚 Structured Topics")
        for item in st.session_state["topics"]:
            st.markdown(f"**📘 {item['chapter']}**")
            for topic in item['topics']:
                st.markdown(f"- {topic}")

        st.markdown("### 📝 Summarized Notes")
        for chapter, chapter_topics in st.session_state["summaries"].items():
            st.markdown(f"**🧾 {chapter}**")
            for topic, bullets in chapter_topics.items():
                st.markdown(f"**🔹 {topic}**")
                for bullet in bullets:
                    st.markdown(f"- {bullet}")

        st.markdown("### ❓ Auto-Generated MCQs")
        for chapter, chapter_data in st.session_state["mcqs"].items():
            st.markdown(f"**📖 {chapter}**")
            for topic, question_list in chapter_data.items():
                st.markdown(f"**🧠 Topic: {topic}**")
                for q in question_list:
                    st.markdown(f"**Q:** {q['question']}")
                    for i, option in enumerate(q['options']):
                        st.markdown(f"- {chr(65+i)}. {option}")
                    st.markdown("---")

        st.info("Ready to take the mock exam?")
        if st.button("🎯 Start Exam"):
            st.session_state["start_exam"] = True
            st.rerun()

    # --- EXAM UI ---
    if st.session_state["start_exam"]:
        st.markdown("## 🧪 Mock Exam")
        st.info("Answer the following questions:")

        mcqs = st.session_state["exam_data"]["mcqs"]
        user_answers = {}

        for chapter, chapter_data in mcqs.items():
            st.markdown(f"### 📖 {chapter}")
            for topic, question_list in chapter_data.items():
                st.markdown(f"#### 🧠 {topic}")
                for idx, q in enumerate(question_list):
                    question_id = f"{chapter}_{topic}_{idx}"
                    user_answers[question_id] = st.radio(
                        f"**Q: {q['question']}**",
                        options=[f"{chr(65+i)}. {opt}" for i, opt in enumerate(q["options"])],
                        key=question_id
                    )
                    st.markdown("---")

        if st.button("✅ Submit Answers"):
            correct = 0
            total = 0
            summary = []

            for chapter, chapter_data in mcqs.items():
                for topic, question_list in chapter_data.items():
                    for idx, q in enumerate(question_list):
                        question_id = f"{chapter}_{topic}_{idx}"
                        user_ans = st.session_state.get(question_id, "")
                        correct_ans_index = ord(q["answer"]) - 65
                        correct_option = q["options"][correct_ans_index]
                        user_selected = user_ans.split(". ", 1)[-1] if ". " in user_ans else user_ans

                        summary.append({
                            "question": q["question"],
                            "your_answer": user_selected,
                            "correct_answer": correct_option,
                            "is_correct": user_selected == correct_option
                        })

                        total += 1
                        if user_selected == correct_option:
                            correct += 1

            st.markdown("---")
            st.markdown("## ✅ Result Summary")
            st.write(f"**🎯 You scored {correct} out of {total}**")

            for result in summary:
                status = "✅ Correct" if result["is_correct"] else "❌ Incorrect"
                st.markdown(f"""
                **Q:** {result['question']}  
                - **Your Answer:** {result['your_answer']}  
                - **Correct Answer:** {result['correct_answer']}  
                - **Result:** {status}  
                ---
                """)

if __name__ == "__main__":
    main()
