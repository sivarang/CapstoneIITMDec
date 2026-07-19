"""
LangGraph State

Shared state across all agents.
"""

from typing import Annotated, Literal, TypedDict

from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

greeted: bool

from typing import TypedDict, Optional, List

class AgentState(TypedDict, total=False):
    messages: list
    greeted: bool
    question_count: int
    next_action: str
    resolved: bool
    router_vendor: str
    router_model: str
    retrieved_context: str
    manual_found: bool
    escalation_required: bool
    in_scope: bool
    
class RouterSupportState(TypedDict):
    """
    Global workflow state.
    """

    # Conversation
    messages: Annotated[list[BaseMessage], add_messages]

    # Session
    session_id: str

    # Router Information
    router_vendor: str
    router_model: str

    router_identified: bool

    # User Problem

    issue: str

    # RAG
    retrieved_context: str
    manual_found: bool

    # Workflow Control
    question_count: int

    next_action: Literal[
        "ASK",
        "USE_RAG",
        "FINISH",
        "ESCALATE",
    ]

    # Flags
    resolved: bool
    escalation_required: bool
    in_scope: bool
    greeted: bool

    greeted = False