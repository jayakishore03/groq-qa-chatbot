import streamlit as st
import requests

# === CONFIG ===
GROQ_API_KEY = "your api key"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-8b-8192"

# === STYLING ===
st.set_page_config(page_title="Groq Q&A Chatbot", layout="centered")

st.markdown("""
    <style>
    body {
        background-image: url('assets\chatbot_bg.png');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        padding: 0;
        margin: 0;
        height: 100vh;
    }
    .question-box input {
        padding: 1rem;
        font-size: 1.1rem;
        border-radius: 10px;
        border: 2px solid #ccc;
        transition: 0.3s ease;
        background: rgba(255, 255, 255, 0.7);  /* Add slight transparency to input */
    }
    .question-box input:hover {
        border-color: #007bff;
        box-shadow: 0 0 8px rgba(0, 123, 255, 0.2);
    }
    .answer-box {
        background-color: rgba(230, 244, 234, 0.8);  /* Slight opacity for answer box */
        padding: 1.2rem;
        border-radius: 12px;
        margin-top: 1rem;
        border-left: 6px solid #3cc46d;
        font-size: 1.05rem;
        line-height: 1.7;
    }
    .title {
        font-size: 2.3rem;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: bold;
        color: #222;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    .btn {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .btn:hover {
        background-color: #0056b3;
    }
    </style>
""", unsafe_allow_html=True)

# === HEADER ===
st.markdown("<div class='title'>🤖 Q&A Chatbot with Groq + LLM</div>", unsafe_allow_html=True)

# === INPUT ===
user_question = st.text_input("Ask a question:", key="input_box", placeholder="E.g. What is AI?")

# === BUTTON ===
get_answer = st.button("Get Answer", type="primary")

# === FUNCTION ===
def fetch_groq_answer(question):
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Answer the following question."},
        {"role": "user", "content": question}
    ]
    response = requests.post(
        GROQ_API_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": 0.7
        }
    )
    return response.json()

# === HANDLE RESPONSE ===
if get_answer and user_question.strip():
    with st.spinner("Thinking... 🤔"):
        data = fetch_groq_answer(user_question)
        if "choices" in data:
            answer = data["choices"][0]["message"]["content"]
            st.markdown("<h4>Answer:</h4>", unsafe_allow_html=True)
            st.markdown(f"<div class='answer-box'>{answer}</div>", unsafe_allow_html=True)
        else:
            st.error("Failed to get a response from Groq API.")
            st.json(data)
