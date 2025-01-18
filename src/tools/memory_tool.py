import os

import psycopg2
from dotenv import load_dotenv
from langchain.tools import StructuredTool
from langchain_core.tools import ToolException

from src.memory.data import AddMemory, Category

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASS"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
)


def modify_memory(
    id: str, memory: str, category: str, action: str, memory_old: str = None
):
    """
    Function to modify memory in the database
    """
    print(
        f"Modifying long term memory for {id} with action {action} and category {Category(category).value}"
    )
    if Category(category).value not in [
        "Course Likes",
        "Course Dislikes",
        "Branch",
        "Clubs",
        "Person Attributes",
    ]:
        return "Invalid category choose from: Course Likes, Course Dislikes, Branch, Clubs, Person Attributes"
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS longterm_memory (
            id VARCHAR(255) NOT NULL,
            memory VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL
        );
        """
    )
    if action == "Create":
        cur.execute(
            f"""
            INSERT INTO longterm_memory (id, memory, category)
            VALUES ('{id}', '{memory}', '{Category(category).value}');
            """
        )
        conn.commit()
        return "Memory created successfully"
    elif action == "Update":
        cur.execute(
            f"""
            UPDATE longterm_memory
            SET memory = '{memory}'
            WHERE id = '{id}' AND memory = '{memory_old}';
            """
        )
        conn.commit()
        return "Memory updated successfully"
    elif action == "Delete":
        cur.execute(
            f"""
            DELETE FROM longterm_memory
            WHERE id = '{id}' AND memory = '{memory_old}' AND category = '{Category(category).value}';
            """
        )
        conn.commit()
        return "Memory deleted successfully"
    else:
        return "Invalid action"


def fetch_long_term_memory(id: str) -> list[AddMemory]:
    """
    Function to fetch long term memory from the database
    """
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT memory, category
        FROM longterm_memory
        WHERE id = '{id}';
        """
    )
    rows = cur.fetchall()
    print(f"Fetched long term memory for {id} = {rows}")
    return [
        AddMemory(id=id, memory=row[0], category=row[1], action="Create")
        for row in rows
    ]


def reset_long_term_memory(id: str) -> None:
    """
    Function to reset long term memory from the database
    """
    cur = conn.cursor()
    cur.execute(
        f"""
        DELETE FROM longterm_memory
        WHERE id = '{id}';
        """
    )
    conn.commit()
    print(f"Reset long term memory for {id}")


def _handle_tool_error(error: ToolException) -> str:
    return f"The following errors occurred during tool execution: `{error.args[0]}`"


tool_modify_memory = StructuredTool.from_function(
    func=modify_memory,
    name="modify_memory",
    description="Modify the long term memory of a user",
    args_schema=AddMemory,
    handle_tool_error=_handle_tool_error,
)
