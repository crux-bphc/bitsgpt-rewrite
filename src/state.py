from typing import Annotated, Optional

from langgraph.graph.message import add_messages
from src.memory.data import AddMemory
from typing_extensions import TypedDict


class State(TypedDict):
    user_id: str
    messages: Annotated[list, add_messages]
    chat_history: Optional[str]
    long_term_memories: Optional[list[AddMemory]]
