import os

import psycopg2
from dotenv import load_dotenv
from langchain.tools import StructuredTool
from langchain_core.tools import ToolException

from src.memory.data import Category, LongTermMemory

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASS"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
)


def add_long_term_memory(
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
        CREATE TABLE IF NOT EXISTS long_term_memory (
            id VARCHAR(255) NOT NULL,
            memory VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL
        );
        """
    )
    if action == "Create":
        cur.execute(
            f"""
            INSERT INTO long_term_memory (id, memory, category)
            VALUES ('{id}', '{memory}', '{Category(category).value}');
            """
        )
        conn.commit()
        return "Memory created successfully"
    elif action == "Update":
        cur.execute(
            f"""
            UPDATE long_term_memory
            SET memory = '{memory}'
            WHERE id = '{id}' AND memory = '{memory_old}';
            """
        )
        conn.commit()
        return "Memory updated successfully"
    elif action == "Delete":
        cur.execute(
            f"""
            DELETE FROM long_term_memory
            WHERE id = '{id}' AND memory = '{memory_old}' AND category = '{Category(category).value}';
            """
        )
        conn.commit()
        return "Memory deleted successfully"
    else:
        return "Invalid action"


def fetch_long_term_memory(id: str) -> list[LongTermMemory]:
    """
    Function to fetch long term memory from the database
    """
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT memory, category
        FROM long_term_memory
        WHERE id = '{id}';
        """
    )
    rows = cur.fetchall()
    print(f"Fetched long term memory for {id} = {rows}")
    return [
        LongTermMemory(id=id, memory=row[0], category=row[1], action="Create")
        for row in rows
    ]


def reset_long_term_memory(id: str) -> None:
    """
    Function to reset long term memory from the database
    """
    cur = conn.cursor()
    cur.execute(
        f"""
        DELETE FROM long_term_memory
        WHERE id = '{id}';
        """
    )
    conn.commit()
    print(f"Reset long term memory for {id}")
    cur.close()


def parse_long_term_memory(memory: list[LongTermMemory]) -> str:
    """
    Function to parse memory from the database.
    """
    memory_dict = {}
    for mem in memory:
        if Category(mem.category).value not in memory_dict:
            memory_dict[Category(mem.category).value] = []
        memory_dict[Category(mem.category).value].append(mem.memory)
    long_term_memory = ""
    for category in memory_dict:
        long_term_memory += f"{category}:\n"
        for mem in memory_dict[category]:
            long_term_memory += f"- {mem}\n"
    return long_term_memory
