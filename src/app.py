from langgraph.graph import StateGraph, END
from .state import State
from .nodes import intent_classifier, course_query, general_campus_query, not_related_query


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

        graph.set_entry_point("intent_classifer")

        def intent_router(state):
            if "course" in state["messages"][-1].content.lower():
                return "course_query"
            elif "campus" in state["messages"][-1].content.lower():
                return "general_campus_query"
            else:
                return "not_related_query"
            
        
        graph.add_conditional_edges("intent_classifer", intent_router)

        graph.add_edge("course_query", END)
        graph.add_edge("general_campus_query", END)
        graph.add_edge("not_related_query", END)

        return graph