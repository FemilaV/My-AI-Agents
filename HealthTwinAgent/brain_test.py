import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a proactive health twin. You notice a meeting starts in 10 minutes and the user is low on protein."},
        {"role": "user", "content": "What should I do?"}
    ],
    model="llama-3.3-70b-versatile",
)

print(chat_completion.choices[0].message.content)