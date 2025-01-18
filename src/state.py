from typing import Annotated, Optional

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from src.memory.data import LongTermMemory


class State(TypedDict):
    user_id: str
    messages: Annotated[list[AIMessage | HumanMessage], add_messages]
    chat_history: Optional[str]
    long_term_memories: Optional[list[LongTermMemory]]
