import os

import psycopg2
from dotenv import load_dotenv
from langchain.tools import StructuredTool

from src.memory.data import AddMemory

load_dotenv()


def modify_memory(
    id: str, memory: str, category: str, action: str, memory_old: str = None
):
    """
    Function to modify memory in the database
    """
    print(f"Modifying memory for {id} with action {action}")
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASS"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )
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
            VALUES ('{id}', '{memory}', '{category}');
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
            WHERE id = '{id}' AND memory = '{memory_old}' AND category = '{category}';
            """
        )
        conn.commit()
        return "Memory deleted successfully"
    else:
        return "Invalid action"


tool_modify_memory = StructuredTool.from_function(
    func=modify_memory,
    name="modify_memory",
    description="Modify the long term memory of a user",
    args_schema=AddMemory,
)
