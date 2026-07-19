"""
Escalation Agent

Summarizes troubleshooting when escalation is required.
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)

llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0
)

from app.agents.prompts import load_prompt

SYSTEM_PROMPT = load_prompt("escalation.md")
from app.utils.logger import (
    log_agent_start,
    log_agent_end,
    log_error,
)
def escalation_agent(state):
    log_agent_start("Escalation Agent")

    conversation = []

    for msg in state["messages"]:

        role = (
            "User"
            if isinstance(msg, HumanMessage)
            else "Assistant"
        )

        conversation.append(
            f"{role}: {msg.content}"
        )

    prompt = f"""
Create a concise ISP escalation summary.

Include

• Customer issue

• Checks completed

• LED observations

• Likely cause

• Recommendation

Conversation

{chr(10).join(conversation)}
"""

    response = llm.invoke(
        [
            SystemMessage(content=prompt)
        ]
    )

    state["messages"].append(
        AIMessage(
            content=response.content
        )
    )

    state["resolved"] = False

    state["escalation_required"] = True
    state["next_action"] = "FINISH"
    return state