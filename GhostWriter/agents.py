"""
GhostWriter – Agentic Blog Generation System

Pipeline:
1. Researcher Agent (Tavily + Crawl4AI + fast LLM)
2. Writer Agent (local LLM)
3. Editor Agent (single OpenAI call)

Design goals:
- Cost efficiency
- Deterministic outputs
- Production-safe execution
"""


import os
import asyncio
import time
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from web_tools import search_tool, scrape_website


# -----------------------------
# LLM SETUP
# -----------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI → ONLY for final editing (fast, one call)
openai_llm = ChatOpenAI(
    model="gpt-4o",
    api_key=OPENAI_API_KEY,
    temperature=0
)

# Local LLM → writing (cheap)
local_llm = ChatOllama(
    model="llama3.2",
    temperature=0.4
)

# fast LLM → research 
fast_llm = ChatOllama(
    model="phi3:mini",
    temperature=0.2
)

# -----------------------------
# RESEARCHER AGENT
# -----------------------------
def researcher_agent(state):
    print("\n--- AGENT: RESEARCHER (Tavily + httpx) ---")
    total_start = time.perf_counter()

    topic = state["topic"]

    # 1️⃣ Tavily Search
    t0 = time.perf_counter()
    search_results = search_tool.invoke(topic)
    print(f"[TIMER] Tavily search: {time.perf_counter() - t0:.2f}s")

    urls = [
        r["url"]
        for r in search_results
        if isinstance(r, dict) and "url" in r
    ][:3]  # hard limit for speed

    print(f"Found {len(urls)} URLs")

    # 2️⃣ Scrape URLs (async)
    async def scrape_all():
        tasks = [scrape_website(url) for url in urls]
        return await asyncio.gather(*tasks)

    t0 = time.perf_counter()
    scraped_pages = asyncio.run(scrape_all())
    print(f"[TIMER] Scraping: {time.perf_counter() - t0:.2f}s")

    # 3️⃣ Reduce token size aggressively
    combined_text = "\n\n".join(
        page[:800] for page in scraped_pages if page
    )

    # 4️⃣ ONE LLM CALL → Research + Outline
    prompt = f"""
You are a research assistant.

Topic: {topic}

Using the web research below, produce TWO sections exactly in this format:

SECTION 1 — RESEARCH NOTES
- Bullet points only
- Key facts
- Trends
- Statistics (numbers if available)
- Expert or industry opinions
- Max 200 words

SECTION 2 — BLOG OUTLINE
- H1 title
- H2 section headings
- Logical flow
- No explanations

Rules:
- Be factual
- No fluff
- No repetition

WEB RESEARCH:
{combined_text}
"""

    print("Summarizing research + generating outline (Fast LLM)...")
    t0 = time.perf_counter()
    try:
        response = fast_llm.invoke(prompt)
    except Exception:
        response = local_llm.invoke(prompt)

    print(f"[TIMER] Research + outline: {time.perf_counter() - t0:.2f}s")

    text = response.content

    # 5️⃣ Parse output safely
    research_notes = ""
    outline = ""

    if "SECTION 2" in text:
        parts = text.split("SECTION 2")
        research_notes = (
            parts[0]
            .replace("SECTION 1 — RESEARCH NOTES", "")
            .strip()
        )
        outline = (
            parts[1]
            .replace("— BLOG OUTLINE", "")
            .strip()
        )
    else:
        research_notes = text
        outline = "Introduction\nMain Content\nConclusion"

    print(f"[TIMER] TOTAL researcher: {time.perf_counter() - total_start:.2f}s")

    return {
        "research_notes": research_notes,
        "outline": outline
    }

# -----------------------------
# WRITER AGENT (LOCAL)
# -----------------------------
def writer_agent(state):
    print("\n--- AGENT: WRITER (Local LLM) ---")
    t0 = time.perf_counter()

    prompt = f"""
Write a structured, engaging blog post using:

OUTLINE:
{state['outline']}

RESEARCH NOTES:
{state['research_notes']}

Requirements:
- Strong introduction and conclusion
- Clear section headings
- Professional tone
- Logical flow
"""

    response = local_llm.invoke(prompt)

    print(f"[TIMER] Writing: {time.perf_counter() - t0:.2f}s")

    return {
        "content": response.content
    }

# -----------------------------
# FINAL EDITOR AGENT (PAID – ONCE)
# -----------------------------
def editor_agent(state):
    print("\n--- AGENT: FINAL EDITOR (OpenAI GPT-4o) ---")

    # Ensure ONLY one paid call
    if state["revision_count"] >= 1:
        return state

    t0 = time.perf_counter()

    prompt = f"""
You are a professional editor.

TASK:
Polish the blog post below.

RULES (STRICT):
- Output ONLY the final edited blog post
- Do NOT explain changes
- Do NOT add summaries
- Do NOT add bullet points
- Do NOT add commentary before or after

BLOG POST:
{state['content']}
"""

    response = openai_llm.invoke(prompt)

    print(f"[TIMER] Editing: {time.perf_counter() - t0:.2f}s")

    return {
        "content": response.content,
        "revision_count": state["revision_count"] + 1
    }
