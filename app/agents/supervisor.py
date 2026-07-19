"""
Supervisor Agent

Responsibilities
----------------
✓ Greet the user
✓ Restrict scope to networking
✓ Ask one question at a time
✓ Decide whether RAG is needed
✓ Escalate after 5 questions
✓ Finish when issue resolved
"""

import json

from langchain_openai import ChatOpenAI

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    BaseMessage,
)

from app.agents.prompts import load_prompt

#from app.tools.router_identifier import identify_router
from langchain_core.messages import AIMessage, HumanMessage

from app.utils.logger import (
    log_agent_start,
    log_agent_end
)
# -------------------------------------------------------
# LLM
# -------------------------------------------------------

llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0
)


SYSTEM_PROMPT = load_prompt("supervisor.md")


# -------------------------------------------------------
# Helper
# -------------------------------------------------------

def format_messages(messages: list[BaseMessage]) -> str:
    """
    Convert LangChain messages into readable conversation.
    """

    output = []

    for msg in messages:

        if isinstance(msg, HumanMessage):
            role = "User"

        elif isinstance(msg, AIMessage):
            role = "Assistant"

        else:
            role = "System"

        output.append(
            f"{role}: {msg.content}"
        )

    return "\n".join(output)

from app.utils.logger import (
    logger,
    log_agent_start,
    log_agent_end,
    log_router,
    log_error,
)
# -------------------------------------------------------
# Supervisor
# -------------------------------------------------------
from langchain_core.messages import AIMessage


def supervisor(state):

    print("Supervisor State")
    print("router_model :", state.get("router_model"))
    print("router_vendor:", state.get("router_vendor"))
    print("next_action  :", state.get("next_action"))

    messages = state["messages"]

    #
    # Greeting
    #
    if len(messages) == 1:

        greeting = """
Hello!

Welcome to NetAssist.

I currently support:

• TP-Link Archer C5
• Netgear D7000

Please describe your issue.
If possible, include your router model.
"""

        messages.append(AIMessage(content=greeting))

        state["next_action"] = "ASK"
        return state
    # Issue already resolved
    if state.get("resolved"):
        state["next_action"] = "FINISH"
        return state
    # Issue already escalted
    if state.get("escalation_required"):
        messages.append(
            AIMessage(
                content=(
                    "This issue has already been escalated to Tier2 support."
                    "Please wait for an engineet to contact you"
                    "If you would like to hel with a new issue let me know"
                )
            )
        )
        state["next_action"] = "FINISH"
        return state

    # Too many questions
    if state.get("question_count", 0) >= 10:
        state["next_action"] = "ESCALATE"
        return state
    #
    # Capture router model
    #
    if not state.get("router_model"):

        last_message = ""

        if isinstance(messages[-1], HumanMessage):
            last_message = messages[-1].content
        print("=" * 50)
        print("Last message:", repr(last_message))

        router = identify_router(last_message)

        print("Router identified:", router)
        print("=" * 50)
        router = identify_router(last_message)

        if router:

            state["router_vendor"] = router["vendor"]
            state["router_model"] = router["model"]

            messages.append(
                AIMessage(
                    content=f"I identified your router as {router['vendor']} {router['model']}. Let's troubleshoot your issue."
                )
            )

        else:

            messages.append(
                AIMessage(
                    content="""Which router are you using?

Supported models:
• TP-Link Archer C5
• Netgear D7000"""
                )
            )

            state["next_action"] = "ASK"
            return state

    #
    # Continue troubleshooting
    #
    state["next_action"] = "USE_RAG"

    return state

import re

def identify_router(text: str):
    print("INPUT:", repr(text))

    text = text.lower()
    print("LOWER:", repr(text))

    if any(x in text for x in ["tp-link", "tplink", "archer", "c5"]):
        print("Matched TP-Link")
        return {
            "vendor": "TP-Link",
            "model": "Archer C5"
        }

    if any(x in text for x in ["netgear", "d7000"]):
        print("Matched Netgear")
        return {
            "vendor": "Netgear",
            "model": "D7000"
        }

    print("No match")
    return None