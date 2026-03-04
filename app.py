import streamlit as st
from groq import Groq
import os
import re

# ---------------- SETUP ----------------

st.set_page_config(page_title="AI Study Buddy", layout="wide")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- DARK THEME ----------------

st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.title("📚 AI Study Buddy")

feature = st.sidebar.radio(
    "Choose Feature",
    ["Explain Topic", "Summarize Notes", "Generate Quiz", "Generate Flashcards"]
)

# ---------------- FEATURE CHANGE HANDLING ----------------

if "feature_state" not in st.session_state:
    st.session_state.feature_state = feature

if st.session_state.feature_state != feature:
    st.session_state.clear()
    st.session_state.feature_state = feature
    st.rerun()

# ---------------- CLEAR FUNCTION ----------------

def clear_all():
    st.session_state.input_text = ""
    st.session_state.pop("output", None)
    st.session_state.pop("submitted", None)

# ---------------- MAIN ----------------

st.title("📖 AI Study Buddy")

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

user_input = st.text_area(
    "Enter your topic or paste your notes here:",
    key="input_text",
    height=200
)

col1, col2 = st.columns(2)

generate = col1.button("🚀 Generate")
clear_btn = col2.button("🗑 Clear", on_click=clear_all)

# ---------------- GENERATE ----------------

if generate and user_input.strip():

    if feature == "Explain Topic":
        prompt = f"Explain clearly for students:\n{user_input}"

    elif feature == "Summarize Notes":
        prompt = f"Summarize into bullet points:\n{user_input}"

    elif feature == "Generate Quiz":
        prompt = f"""
Create 5 multiple choice questions.
Format exactly like this:

Q1: Question
a) Option
b) Option
c) Option
d) Option
Answer: a

Topic:
{user_input}
"""

    elif feature == "Generate Flashcards":
        prompt = f"""
Create 5 flashcards.
Format exactly like this:

Q1: Question
A1: Answer

Topic:
{user_input}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful study assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    st.session_state.output = response.choices[0].message.content
    st.session_state.submitted = False
    st.rerun()

# ---------------- DISPLAY OUTPUT ----------------

if "output" in st.session_state:

    st.markdown("---")
    st.subheader("📖 Output")

    output = st.session_state.output

    # ---------------- QUIZ ----------------
    if feature == "Generate Quiz":

        pattern = r"(Q\d+:.*?Answer:\s*[abcd])"
        matches = re.findall(pattern, output, re.DOTALL)

        questions = []

        for block in matches:
            lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
            question = lines[0]
            options = lines[1:5]
            answer_line = lines[-1]
            correct = answer_line.split(":")[1].strip().lower()
            questions.append((question, options, correct))

        score = 0

        for i, (question, options, correct) in enumerate(questions):

            st.markdown(f"### {question}")

            choice = st.radio(
                "Select answer:",
                options,
                key=f"q{i}"
            )

            if st.session_state.get("submitted"):
                if choice.lower().startswith(correct):
                    st.success("✅ Correct")
                    score += 1
                else:
                    st.error(f"❌ Incorrect. Correct answer: {correct.upper()}")

            st.markdown("---")

        if not st.session_state.get("submitted"):
            if st.button("Submit Quiz"):
                st.session_state.submitted = True
                st.rerun()
        else:
            percentage = (score / len(questions)) * 100 if questions else 0
            st.success(f"🏆 Score: {score} / {len(questions)}")
            st.info(f"📊 Percentage: {percentage:.2f}%")

    # ---------------- FLASHCARDS ----------------
    elif feature == "Generate Flashcards":

        pattern = r"(Q\d+:.*?A\d+:.*?)(?=\nQ\d+:|\Z)"
        matches = re.findall(pattern, output, re.DOTALL)

        for block in matches:
            lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
            question = lines[0]
            answer = lines[1] if len(lines) > 1 else ""

            st.markdown(f"### 🟦 {question}")
            with st.expander("Show Answer"):
                st.success(answer)

    # ---------------- OTHER FEATURES ----------------
    else:
        st.markdown(output)

# ---------------- FOOTER ----------------

st.markdown("---")
st.markdown("👨‍💻 Developed by SREESHAA | 2026")