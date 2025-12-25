"""
This module acts as an orchestration layer, combining meal data and calendar events
to generate high-level coaching advice using Groq's LLM.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_coach_advice(meal_macros, upcoming_events):
    """
    Combines meal macros and upcoming events to generate proactive health advice.
    Uses the llama-3.3-70b-versatile model for reasoning.
    """
    prompt = f"""
    You are a Personal Health Twin. 
    LATEST MEAL: {meal_macros}
    UPCOMING MEETINGS: {upcoming_events}

    Analyze the situation:
    1. Does the user have enough energy/protein for these meetings?
    2. Is there a high-stress window coming up?
    3. Provide one proactive, short tip (max 2 sentences).
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    return response.choices[0].message.content

# TEST DATA (Eventually these will be variables from your other scripts)
current_meal = {"protein": 20, "carbs": 25, "fat": 10}
my_meetings = ["2:00 PM - Board Review (High Stress)", "3:30 PM - Project Sync"]

advice = get_coach_advice(current_meal, my_meetings)
print("--- COACH ADVICE ---")
print(advice)