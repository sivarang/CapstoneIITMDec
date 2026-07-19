from uuid import uuid4

from fastapi import APIRouter

from langchain_core.messages import HumanMessage

from app.graph.workflow import graph
from app.models.schemas import ChatRequest

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):

    session_id = request.session_id or str(uuid4())

    # First request in conversation
    if request.session_id is None:

        state = {
            "messages": [
                HumanMessage(content=request.message)
            ],
            "session_id": session_id,
            "router_vendor": "",
            "router_model": "",
            "router_identified": False,
            "issue": "",
            "retrieved_context": "",
            "manual_found": False,
            "question_count": 0,
            "next_action": "ASK",
            "resolved": False,
            "escalation_required": False,
            "in_scope": True,
            "greeted": False,
        }

    # Existing conversation
    else:

        state = {
            "messages": [
                HumanMessage(content=request.message)
            ]
        }

    config = {
        "configurable": {
            "thread_id": session_id
        }
    }

    result = graph.invoke(
        state,
        config=config
    )

    print("=" * 60)
    print("Returned State")
    print(result)
    print("=" * 60)

    return {
        "session_id": session_id,
        "messages": [
            m.content
            for m in result.get("messages", [])
        ],
        "resolved": result.get("resolved", False),
        "next_action": result.get("next_action", "ASK"),
        "question_count": result.get("question_count", 0)
    }
