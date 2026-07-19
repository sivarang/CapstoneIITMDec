from uuid import uuid4

from fastapi import APIRouter

from langchain_core.messages import HumanMessage

from app.graph.workflow import graph

from app.models.schemas import ChatRequest

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):

    session_id = request.session_id or str(uuid4())

    result = graph.invoke(
        state,
        config={
            "configurable": {
                "thread_id": session_id
            }
        }
    )

    print("Returned State:")
    print(result)

    #session_id = request.session_id or str(uuid4())

    if request.session_id is None:
        state = {
            "messages": [HumanMessage(content=request.message)],
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
    else:
        state = {
            "messages": [HumanMessage(content=request.message)]
        }

    result = graph.invoke(
        state,
        config=config
    )

    return {
        "session_id": session_id,
        "messages": [
            m.content
            for m in result["messages"]
        ],
        "resolved": result["resolved"],
        "next_action": result["next_action"],
        "question_count": result["question_count"]
    }
