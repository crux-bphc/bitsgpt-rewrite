from langgraph.graph import END, StateGraph

from .nodes import (
    course_query,
    general_campus_query,
    intent_classifier,
    not_related_query,
    long_term_memory,
)
from .state import State


class BitsGPT:
    def __init__(self):
        self.graph = self.create_graph()
        self.app = self.graph.compile()

    def create_graph(self) -> StateGraph:
        graph = StateGraph(State)

        graph.add_node("intent_classifer", intent_classifier)
        graph.add_node("course_query", course_query)
        graph.add_node("general_campus_query", general_campus_query)
        graph.add_node("not_related_query", not_related_query)
        graph.add_node("long_term_memory", long_term_memory)

        graph.set_entry_point("intent_classifer")

        def intent_router(state):
            if "course" in state["messages"][-1].content.lower():
                return "course_query"
            elif "campus" in state["messages"][-1].content.lower():
                return "general_campus_query"
            else:
                return "not_related_query"

        graph.add_conditional_edges("intent_classifer", intent_router)

        graph.add_edge(
            "course_query",
            "long_term_memory",
        )
        graph.add_edge(
            "general_campus_query",
            "long_term_memory",
        )
        graph.add_edge(
            "not_related_query",
            "long_term_memory",
        )
        graph.add_edge(
            "long_term_memory",
            END,
        )
        return graph
