"""
LangGraph Workflow
"""

from langgraph.graph import StateGraph
from langgraph.graph import START, END
from langgraph.checkpoint.memory import MemorySaver


from app.graph.state import RouterSupportState

from app.agents.supervisor import supervisor
from app.agents.troubleshooter import troubleshooter
from app.agents.escalation import escalation_agent
from app.agents.rag_agent import rag_agent

# ------------------------------------------------
# Build Graph
# ------------------------------------------------

builder = StateGraph(RouterSupportState)


builder.add_node(
    "supervisor",
    supervisor
)


builder.add_node(
   "troubleshooter",
   troubleshooter
)

builder.add_node(
    "rag",
    rag_agent
)

builder.add_node(
    "escalation",
    escalation_agent
)


# Start

builder.add_edge(
    START,
    "supervisor"
)


# ------------------------------------------------
# Routing
# ------------------------------------------------

def supervisor_router(state):

    action = state.get(
        "next_action"
    )


    if action == "ASK":

        return END

    if action == "USE_RAG":

        return "rag"

    if action == "TROUBLESHOOT":

        return "troubleshooter"


    if action == "ESCALATE":

        return "escalation"


    if action == "FINISH":

        return END


    return END



# Troubleshooter returns to supervisor

builder.add_edge(
    START,
    "supervisor"
)

builder.add_conditional_edges(
    "supervisor",
    supervisor_router
)

builder.add_edge(
    "rag",
    "troubleshooter"
)

builder.add_edge(
    "troubleshooter",
    END
)

builder.add_edge(
    "escalation",
    END
)



# ------------------------------------------------
# Memory
# ------------------------------------------------

memory = MemorySaver()


graph = builder.compile(
    checkpointer=memory
)