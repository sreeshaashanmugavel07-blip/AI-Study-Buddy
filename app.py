import streamlit as st
from groq import Groq
import os

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Page configuration
st.set_page_config(page_title="AI Study Buddy", layout="centered")

st.title("📚 AI-Powered Study Buddy")
st.write("Explain topics, summarize notes, and generate quizzes or flashcards.")

# Feature selection
feature = st.selectbox(
    "Select a Feature",
    [
        "Explain Topic",
        "Summarize Notes",
        "Generate Quiz",
        "Generate Flashcards"
    ]
)

# User input
user_input = st.text_area("Enter your topic or paste your notes here:")

# Generate button
if st.button("Generate"):

    if not user_input.strip():
        st.warning("Please enter some content first.")
    else:

        # Create prompt based on feature
        if feature == "Explain Topic":
            prompt = f"Explain this topic clearly and simply for students:\n\n{user_input}"

        elif feature == "Summarize Notes":
            prompt = f"Summarize this into concise bullet points:\n\n{user_input}"

        elif feature == "Generate Quiz":
            prompt = f"Create 5 quiz questions with answers based on:\n\n{user_input}"

        elif feature == "Generate Flashcards":
            prompt = f"Create 5 flashcards in Question and Answer format based on:\n\n{user_input}"

        with st.spinner("Generating..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",  # Current supported model
                    messages=[
                        {"role": "system", "content": "You are a helpful and clear study assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1024
                )

                output = response.choices[0].message.content

                st.subheader("📖 Output")
                st.write(output)

            except Exception as e:
                st.error(f"Error: {e}")