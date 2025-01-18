from langchain_core.messages import AIMessage

from .agents import Agents
from .memory.long_term_memory import parse_long_term_memory
from .memory.short_term_memory import add_short_term_memory
from .state import State

agents = Agents()


def intent_classifier(state: State):
    query = state["messages"][-agents.depths["intent_classifier"]].content
    result = AIMessage(agents.intent_classifier(query, state.get("chat_history", "")))
    return {"messages": [result]}


def course_query(state: State):
    query = state["messages"][-agents.depths["course_query"]].content
    result = AIMessage("Course query not implemented yet")
    # Add short term memory here once implemented.
    return {"messages": [result]}


def general_campus_query(state: State):
    query = state["messages"][-agents.depths["general_campus_query"]].content
    result = AIMessage(
        agents.general_campus_query(query, state.get("chat_history", ""))
    )
    add_short_term_memory(
        state["user_id"],
        query,
        result.content,
        "general_campus_query",
    )
    return {"messages": [result]}


def not_related_query(state: State):
    query = state["messages"][-agents.depths["not_related_query"]].content
    result = AIMessage(
        "I'm sorry, I don't understand the question, if it relates to campus please rephrase."
    )
    add_short_term_memory(
        state["user_id"],
        query,
        "not_related_query",
        "intent_classifier",
    )
    return {"messages": [result]}


def long_term_memory(state: State):
    query = state["messages"][-agents.depths["long_term_memory"]].content
    user_id = state["user_id"]
    long_term_memories = parse_long_term_memory(state.get("long_term_memories", []))
    result = AIMessage(
        agents.long_term_memory(
            user_id,
            query,
            long_term_memories,
        )
    )
    return {"messages": [result]}
