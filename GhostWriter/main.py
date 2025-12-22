# main.py

from langgraph.graph import StateGraph, END
from state import AgentState
from agents import researcher_agent, editor_agent, writer_agent


# -----------------------------
# 1. REVISION DECISION FUNCTION
# -----------------------------
def should_revise(state: AgentState) -> bool:
    """
    Content will not be revise.
    """
    return state["revision_count"] < 1


# -----------------------------
# 2. BUILD THE GRAPH
# -----------------------------
workflow = StateGraph(AgentState)

# Add agent nodes
workflow.add_node("researcher", researcher_agent)
workflow.add_node("writer", writer_agent)
workflow.add_node("editor", editor_agent)

# -----------------------------
# 3. DEFINE FLOW
# -----------------------------

# Entry point
workflow.set_entry_point("researcher")

# Normal flow
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "editor")

# Conditional revision loop
workflow.add_conditional_edges(
    "editor",
    should_revise,
    {
        True: "writer",   # revise again
        False: END        # finish
    }
)

# -----------------------------
# 4. COMPILE
# -----------------------------
app = workflow.compile()


# -----------------------------
# 5. RUN
# -----------------------------
if __name__ == "__main__":
    inputs = {
        "topic": "The importance of mental health",
        "revision_count": 0
    }

    final_state = app.invoke(inputs)
    print(final_state["content"])
