"""
Troubleshooter Agent

Uses the router manual to guide the user.
"""

from langchain_openai import ChatOpenAI

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)

from app.agents.prompts import load_prompt

llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0
)

SYSTEM_PROMPT = load_prompt(
    "troubleshooter.md"
)

from app.utils.logger import (
    log_agent_start,
    log_agent_end,
    log_error,
)

def troubleshooter(state):
    log_agent_start("Troubleshooter")

    history = []

    for msg in state["messages"]:

        role = (
            "User"
            if isinstance(msg, HumanMessage)
            else "Assistant"
        )

        history.append(
            f"{role}: {msg.content}"
        )

    conversation = "\n".join(history)

    prompt = f"""
{SYSTEM_PROMPT}

Router Manual
-------------

{state["retrieved_context"]}

Conversation
------------

{conversation}
"""

    response = llm.invoke(
        [
            SystemMessage(content=prompt)
        ]
    )

    answer = response.content

    state["messages"].append(
        AIMessage(content=answer)
    )
    
    state["next_action"] = "ASK"

    return state