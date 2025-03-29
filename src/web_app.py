import json
import streamlit as st

# Load mock exam from results folder
@st.cache_data
def load_mock_exam():
    try:
        with open("results/mock_exam.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def main():
    st.set_page_config(page_title="PrepPilot Mock Exam", layout="centered")
    st.title("🧠 PrepPilot AI Mock Exam")
    st.markdown("Answer the following questions and submit to see your score.")

    exam = load_mock_exam()

    if not exam:
        st.error("⚠️ No mock exam found in 'results/mock_exam.json'. Please run the pipeline first.")
        return

    st.divider()
    user_answers = {}
    questions = exam.get("questions", [])

    for idx, q in enumerate(questions, 1):
        st.subheader(f"Q{idx}: {q['question']}")
        options = q["options"]
        user_answers[idx] = st.radio("Choose one:", options, key=idx)
        st.markdown("---")

    # Submit button
    if st.button("📩 Submit My Answers"):
        score = 0
        result_summary = []

        for i, q in enumerate(questions, 1):
            correct_option = q["options"][ord(q["answer"].upper()) - 65]
            user_answer = user_answers[i]
            is_correct = user_answer == correct_option
            if is_correct:
                score += 1

            result_summary.append({
                "question": q["question"],
                "your_answer": user_answer,
                "correct_answer": correct_option,
                "is_correct": is_correct
            })

        st.success(f"🎉 You scored {score} out of {len(questions)}")

        # Show detailed breakdown
        for res in result_summary:
            st.write(f"**Q:** {res['question']}")
            st.write(f"✅ Correct Answer: {res['correct_answer']}")
            st.write(f"🧑 Your Answer: {res['your_answer']}")
            if res['is_correct']:
                st.success("✔️ Correct!")
            else:
                st.error("❌ Incorrect")
            st.markdown("---")


if __name__ == "__main__":
    main()
