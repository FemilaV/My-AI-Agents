# 🧬 Health Twin Agent

An AI-powered personal health companion that integrates Computer Vision, Real-time Voice AI, and Calendar Intelligence to provide proactive coaching based on your BMI, daily nutrition, and schedule.

---

## 🚀 Overview

The Health Twin doesn't just talk; it remembers. By combining a persistent state (JSON) with multi-modal inputs, it tracks your nutritional intake from photos and syncs with your Google Calendar to give you timely health advice when you need it most.

---

## 🛠️ Tech Stack

**Brain:** Groq (Llama 3.3 70B) for ultra-fast reasoning.

**Ears/Voice:** LiveKit Agents with Deepgram (STT) and OpenAI (TTS).

**Eyes:** Meta Llama 4 Scout (via Groq) for high-speed meal macro analysis.

**Context:** Google Calendar API for schedule-aware coaching.

**Orchestration:** Python (Asyncio).

---

## 🏗️ Data Pipeline Architecture

The project follows a modular "Source-to-State" data flow:

1. **Ingestion:** User profile setup (`setup_profile.py`) and Image analysis (`test_vision.py`).
2. **Transformation:** Vision models extract calories, protein, fiber, and sugar from unstructured images.
3. **Storage:** Metrics are aggregated and stored in a local `state.json` "mini-warehouse".
4. **Serving:** The `voice_agent.py` pulls current state and calendar data to generate personalized prompts.

---

## ▶️ How to Run

### 1. Setup Environment
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory and add your keys:
```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_key
LIVEKIT_API_SECRET=your_secret
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key
DEEPGRAM_API_KEY=your_deepgram_key
```
*Note: Place your Google Calendar `credentials.json` in the root folder as well.*

### 3. Execution
1. **Initialize Profile:** 
   `python setup_profile.py` (sets your BMI and calorie targets).
2. **Log a Meal:** 
   Place a meal photo as `meal.jpg` and run `python test_vision.py`.
3. **Start the Agent:** 
   `python voice_agent.py dev`
4. **Connect:** 
   Open the **LiveKit Sandbox** or **Agents Playground** link shown in the terminal and click **Connect**.
