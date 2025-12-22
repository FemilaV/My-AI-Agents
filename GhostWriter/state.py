from typing import TypedDict, Optional

class AgentState(TypedDict, total=False):
    """
    Agent State Definition for GhostWriter

    This module defines the shared state schema used by the LangGraph-based
    agentic workflow. The state acts as a single source of truth that is
    incrementally populated and updated by multiple agents (Researcher,
    Writer, Editor) as the graph executes.

    Design Notes:
    - The state is intentionally defined with `total=False` to allow partial
    initialization at graph entry. Only the fields required at time = 0
    (e.g., `topic`, `revision_count`) must be provided by the caller.
    - Other fields (research notes, outline, content) are generated and
    appended by downstream agents.
    """
    topic: str
    research_notes: str
    outline: str
    content: str
    revision_count: int
