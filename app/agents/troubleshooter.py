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

SYSTEM_PROMPT = load_prompt("troubleshooter.md")

from app.utils.logger import (
    log_agent_start,
    log_agent_end,
    log_error,
)


def troubleshooter(state):

    log_agent_start("Troubleshooter")

    messages = state["messages"]

    #
    # User says issue is fixed
    #
    if isinstance(messages[-1], HumanMessage):

        user = messages[-1].content.lower()

        if any(x in user for x in [
            "working",
            "fixed",
            "resolved",
            "yes working",
            "solved"
        ]):

            state["resolved"] = True
            state["next_action"] = "FINISH"

            messages.append(
                AIMessage(
                    content="I'm glad your issue is resolved!"
                )
            )

            log_agent_end("Troubleshooter")
            return state

    #
    # Build System Prompt
    #

    rag_context = state.get("retrieved_context", "")

    if rag_context:

        system_prompt = f"""
{SYSTEM_PROMPT}

====================================================
Router Manual (Retrieved Context)
====================================================

{rag_context}

====================================================

Use ONLY the information in the retrieved manual when
giving troubleshooting steps.

If the manual does not contain the answer,
say you don't know.
"""

    else:

        system_prompt = SYSTEM_PROMPT

    #
    # Build prompt
    #

    prompt = [
        SystemMessage(content=system_prompt),
        *messages
    ]

    print("Before:", state.get("question_count"))

    #
    # LLM call
    #

    response = llm.invoke(prompt)

    messages.append(response)

    #
    # Increment question count
    #

    state["question_count"] = state.get("question_count", 0) + 1

    print("After:", state["question_count"])

    #
    # Decide next action
    #

    if state["question_count"] >= 5:

        state["next_action"] = "ESCALATE"

    else:

        state["next_action"] = "ASK"

    log_agent_end("Troubleshooter")

    return state