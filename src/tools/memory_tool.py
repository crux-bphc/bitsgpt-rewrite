from langchain.tools import StructuredTool
from langchain_core.tools import ToolException

from src.memory.data import LongTermMemory
from src.memory.long_term_memory import add_long_term_memory


def _handle_tool_error(error: ToolException) -> str:
    return f"The following errors occurred during tool execution: `{error.args[0]}`"


tool_modify_memory = StructuredTool.from_function(
    func=add_long_term_memory,
    name="modify_memory",
    description="Modify the long term memory of a user",
    args_schema=LongTermMemory,
    handle_tool_error=_handle_tool_error,
)
