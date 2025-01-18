import os
import uuid
from datetime import datetime

import psycopg2
from dotenv import load_dotenv

from src.memory.data import ShortTermMemory

load_dotenv()


conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASS"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
)


def add_short_term_memory(id: str, query: str, reply: str, agent: str) -> None:
    """
    Function to add short term memory to the database.
    """
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS short_term_memory (id VARCHAR(255) NOT NULL, message_id VARCHAR(255) NOT NULL, created_at TIMESTAMP NOT NULL, query VARCHAR(255) NOT NULL, reply VARCHAR(255) NOT NULL, agent VARCHAR(255) NOT NULL);
        """
    )
    message_id = str(uuid.uuid4())
    created_at = datetime.now()
    cur.execute(
        f"""
        INSERT INTO short_term_memory (id, message_id, created_at, query, reply, agent)
        VALUES ('{id}', '{message_id}', '{created_at}', '{query}', '{reply}', '{agent}');
        """
    )
    conn.commit()
    cur.close()
    print(f"Short term memory added for {id}")


def fetch_short_term_memory(id: str) -> list[ShortTermMemory]:
    """
    Function to fetch short term memory from the database.
    """
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT * FROM short_term_memory WHERE id = '{id}' ORDER BY created_at DESC LIMIT 5;
        """
    )
    rows = cur.fetchall()
    memory = []
    for row in rows:
        memory.append(
            ShortTermMemory(
                id=row[0],
                message_id=row[1],
                created_at=row[2],
                query=row[3],
                reply=row[4],
                agent=row[5],
            )
        )
    if len(memory) > 5:
        cur.execute(
            f"""
            DELETE FROM short_term_memory WHERE id = '{id}' AND created_at < '{memory[-1]["created_at"]}';
            """
        )
        conn.commit()
    cur.close()
    return memory


def reset_short_term_memory(id: str) -> None:
    """
    Function to reset short term memory from the database.
    """
    cur = conn.cursor()
    cur.execute(
        f"""
        DELETE FROM short_term_memory WHERE id = '{id}';
        """
    )
    conn.commit()
    cur.close()
    print(f"Short term memory reset for {id}")


def parse_short_term_memory(short_term_memory: list[ShortTermMemory]) -> str:
    chat_history = ""
    for i, memory in enumerate(short_term_memory):
        chat_history += (
            f"{i+1} User: {memory.query}\nAgent ({memory.agent}): {memory.reply}\n"
        )
    return chat_history
