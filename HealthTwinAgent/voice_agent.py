"""
This module implements the real-time voice agent for the Health Twin.
It connects to LiveKit, uses Groq for LLM reasoning, Deepgram for STT,
and OpenAI for TTS. It integrates user health state and calendar data.
"""

import os
import asyncio
import json
import logging
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli, voice
from livekit.plugins import openai, deepgram, silero
from cal_agent import get_upcoming_events 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("health-twin")
load_dotenv()

async def entrypoint(ctx: JobContext):
    """
    Main entrypoint for the LiveKit agent.
    Performs initial connection, loads user state, fetches calendar events,
    configures the voice agent with dynamic instructions, and starts the session.
    """
    await ctx.connect()
    
    # 1. Load User State
    with open('state.json', 'r') as f:
        state = json.load(f)
    
    u = state['user_profile']
    c = state['current_day']
    remaining = u['daily_calorie_target'] - c['calories']
    
    # 2. Fetch Calendar
    meetings = await asyncio.to_thread(get_upcoming_events)

    # 3. Intelligent Instructions
    instructions = (
        f"You are the Health Twin of {u['name']}. "
        f"Her BMI is {u['bmi']}. Daily Target: {u['daily_calorie_target']} kcal. "
        f"Today's Intake: {c['calories']}kcal, {c['protein']}g Protein, {c['fiber']}g Fiber, {c['sugar']}g Sugar. "
        f"Daily Limit: {state['user_profile']['daily_calorie_target']}kcal. "
        "If sugar is high (>50g), warn her. If fiber is low (<20g), suggest greens. "
        "Keep it brief and coaching-oriented."
    )

    llm = openai.LLM(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile"
    )

    agent = voice.Agent(instructions=instructions, llm=llm)
    session = voice.AgentSession(vad=silero.VAD.load(), stt=deepgram.STT(), tts=openai.TTS())

    await session.start(agent, room=ctx.room)
    await asyncio.sleep(1)
    
    # 4. Proactive Dynamic Greeting
    greeting = f"Hi {u['name']}! "
    if remaining < 200:
        greeting += "You're nearly at your calorie limit for today. Let's stick to water for now."
    else:
        greeting += f"You have {remaining} calories left today. Ready for your meetings?"
    
    await session.say(greeting, allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))