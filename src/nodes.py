from .agents import Agents
from .state import State

agents = Agents()

def intent_classifier(state: State):
    query = state["messages"][0].content
    result = agents.intent_classifier(query, state["chat_history"])
    return {"messages": [result]}

def course_query(state: State):
    query = state["messages"][0].content
    result = "Course query not implemented yet"
    return {"messages": [result]}

def general_campus_query(state: State):
    query = state["messages"][0].content
    result = agents.general_campus_query(query, state["chat_history"])
    return {"messages": [result]}

def not_related_query(state: State):
    query = state["messages"][0].content
    result = "I'm sorry, I don't understand the question, if it relates to campus please rephrase."
    return {"messages": [result]}    