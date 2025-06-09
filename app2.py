import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os
import time

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are just an AI assistant with Python knowledge.
If the user asks anything other than Python, roast the user.
"""

# Set page config
st.set_page_config(page_title="Gemini Python Bot", page_icon="🧠", layout="centered")

# Inject custom CSS
st.markdown("""
    <style>
    body {
        background-color: #f9f9f9;
    }
    .stChatBubble {
        padding: 1rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        max-width: 80%;
    }
    .user-bubble {
        background-color: #e6f4ea;
        color: #222;
        align-self: flex-end;
        text-align: right;
    }
    .bot-bubble {
        background-color: #e0e7ff;
        color: #111;
        align-self: flex-start;
        text-align: left;
    }
    .typing {
        font-style: italic;
        color: #888;
        margin-top: -10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Description
st.markdown("<h1 style='text-align:center;'>🧠 Python ChatBot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Ask Python questions only. Get roasted if you go off-topic! 😏</p>", unsafe_allow_html=True)
st.markdown("---")

# Initialize chat
if "chat" not in st.session_state:
    model = genai.GenerativeModel("gemini-2.0-flash-001")
    st.session_state.chat = model.start_chat(history=[
        {"role": "user", "parts": [SYSTEM_PROMPT]}
    ])
    st.session_state.messages = []

# User input
user_input = st.text_input("💬 Ask me something Pythonic...", key="input", placeholder="e.g., What is a list comprehension?")

if user_input:
    st.session_state.messages.append(("user", user_input))

    with st.spinner("🤖 Thinking..."):
        response = st.session_state.chat.send_message(user_input)
        bot_reply = response.text.strip()

        # Typing effect (optional delay)
        with st.empty():
            typed_response = ""
            for char in bot_reply:
                typed_response += char
                time.sleep(0.005)
                st.markdown(f"<div class='typing'>{typed_response}</div>", unsafe_allow_html=True)

    st.session_state.messages.append(("bot", bot_reply))

# Display chat history
st.markdown("<div style='display:flex; flex-direction:column;'>", unsafe_allow_html=True)
for role, msg in reversed(st.session_state.messages):
    bubble_class = "user-bubble" if role == "user" else "bot-bubble"
    st.markdown(f"<div class='stChatBubble {bubble_class}'>{msg}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
