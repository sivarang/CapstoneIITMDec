"""
Router Identification Agent

Purpose:
- Identify router vendor/model from user input
- Store router information in state
- Trigger RAG once router is known
"""

from langchain_core.messages import AIMessage


def identify_router(state):

    messages = state.get(
        "messages",
        []
    )

    # Get latest user message
    latest_message = ""

    if messages:
        latest_message = messages[-1].content


    # ---------------------------------------
    # Simple rule-based identification
    # ---------------------------------------
    #
    # Later this can be replaced with:
    # - LLM extraction
    # - Vision model
    # - OCR from router label
    #

    router_found = False


    known_models = [
        "Archer C6",
        "Archer AX10",
        "DIR-825",
        "R7000"
    ]


    for model in known_models:

        if model.lower() in latest_message.lower():

            state["router_model"] = model
            router_found = True
            break



    # ---------------------------------------
    # If router identified
    # ---------------------------------------

    if router_found:

        state["messages"].append(
            AIMessage(
                content=
                f"Thanks. I identified your router model as "
                f"{state['router_model']}. "
                "I will use the router manual to troubleshoot."
            )
        )

        state["next_action"] = "USE_RAG"


        return state



    # ---------------------------------------
    # Ask user
    # ---------------------------------------

    state["messages"].append(
        AIMessage(
            content="""
To provide model-specific troubleshooting,
could you tell me the make and model of your router?

Examples:

• TP-Link Archer C6
• Netgear R7000
• D-Link DIR-825

If you are not sure, you can upload a picture
of the router label later.
"""
        )
    )


    state["next_action"] = "ASK"


    return state