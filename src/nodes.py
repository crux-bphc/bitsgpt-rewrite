from langchain_core.messages import AIMessage

from .agents import Agents
from .state import State

agents = Agents()


def intent_classifier(state: State):
    query = state["messages"][0].content
    result = agents.intent_classifier(query, state.get("chat_history", ""))

    return {"messages": [result]}


def course_query(state: State):
    query = state["messages"][0].content
    result = AIMessage("Course query not implemented yet")
    return {"messages": [result]}


def general_campus_query(state: State):
    query = state["messages"][0].content
    result = agents.general_campus_query(query, state.get("chat_history", ""))
    return {"messages": [result]}


def not_related_query(state: State):
    query = state["messages"][0].content
    result = AIMessage(
        "I'm sorry, I don't understand the question, if it relates to campus please rephrase."
    )
    return {"messages": [result]}


def long_term_memory(state: State):
    query = state["messages"][0].content
    user_id = state["user_id"]
    # parse long term memory here.
    long_term_memories = state.get("long_term_memories", "")
    result = agents.long_term_memory(
        user_id,
        query,
        long_term_memories,
    )
    return {"messages": [result]}
