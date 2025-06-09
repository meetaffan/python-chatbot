import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

messages = [
    {
        "role": "system",
        "content": "You are just an AI assistant with Python knowledge."
        "If the user asks anything other than Python, roast the user."
    }
]

# Interactive loop
print("🔁 AI Chat (type 'exit' to quit)")
while True:
    user_input = input("👤 You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528:free",
        messages=messages
    )

    ai_message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ai_message})

    print(f"🤖 AI: {ai_message}")
