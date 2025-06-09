import streamlit as st
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# Load API keys
load_dotenv()
genai_api_key = os.getenv("GEMINI_API_KEY")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

# Configure APIs
genai.configure(api_key=genai_api_key)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key
)

# Streamlit config
st.set_page_config(page_title="Gemini + DeepSeek Validator", page_icon="🤖", layout="centered")

st.markdown("<h1 style='text-align:center;'>🧠 Python ChatBot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Gemini answers. DeepSeek judges. Python only. 😎 Get roasted if you go off-topic! 😏</p>", unsafe_allow_html=True)
st.markdown("---")

# Session state
if "chat" not in st.session_state:
    model = genai.GenerativeModel("gemini-2.0-flash-001")
    st.session_state.chat = model.start_chat(history=[
        {"role": "user", "parts": ["You are just an AI assistant with Python knowledge. If the user asks anything other than Python, roast the user."]}
    ])
    st.session_state.messages = []

# User input
user_input = st.text_input("💬 Ask me something Pythonic...", key="input", placeholder="e.g., What is a list comprehension?")

def validate_with_deepseek(user_qn, gemini_ans):
    prompt = f"""
User asked: {user_qn}

Gemini answered: {gemini_ans}

You are a Python expert. Is this answer technically correct and related to Python? 
Reply with: "Valid ✅" if it's good, or "Invalid ❌" if it's wrong or off-topic, and provide a reason.
"""
    messages = [
        {"role": "system", "content": "You are just an AI assistant with Python knowledge. If the user asks anything else, roast them."},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528:free",
        messages=messages
    )

    return response.choices[0].message.content.strip()


if user_input:
    st.session_state.messages.append(("user", user_input))

    with st.spinner("🤖 Gemini is thinking..."):
        gemini_response = st.session_state.chat.send_message(user_input).text.strip()

    with st.spinner("🧠 DeepSeek is validating..."):
        deepseek_verdict = validate_with_deepseek(user_input, gemini_response)

    if "valid" in deepseek_verdict.lower():
        st.session_state.messages.append(("bot", f"✅ Gemini: {gemini_response}"))
        st.session_state.messages.append(("validator", f"🧠 DeepSeek: {deepseek_verdict}"))
    else:
        st.session_state.messages.append(("bot", f"❌ Gemini: {gemini_response}"))
        st.session_state.messages.append(("validator", f"🧠 DeepSeek says: {deepseek_verdict}"))

# Display chat history
for role, msg in reversed(st.session_state.messages):
    if role == "user":
        bubble_class = "user-bubble"
    elif role == "bot":
        bubble_class = "bot-bubble"
    else:
        bubble_class = "validator-bubble"

    st.markdown(f"<div class='stChatBubble {bubble_class}'>{msg}</div>", unsafe_allow_html=True)

# Custom CSS
st.markdown("""
    <style>
    .stChatBubble {
        padding: 1rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        max-width: 80%;
    }
    .user-bubble {
        background-color: #e6f4ea;
        color: #222;
        text-align: right;
        align-self: flex-end;
    }
    .bot-bubble {
        background-color: #e0e7ff;
        color: #111;
        text-align: left;
    }
    .validator-bubble {
        background-color: #fff5db;
        color: #333;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)
