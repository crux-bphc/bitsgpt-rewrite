from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Category(str, Enum):
    Course_Like = "Course Likes"
    Course_Dislike = "Course Dislikes"
    Branch = "Branch"
    Clubs = "Clubs"
    Person_Attribute = "Person Attributes"


class Action(str, Enum):
    Create = "Create"
    Update = "Update"
    Delete = "Delete"


class AddMemory(BaseModel):
    id: str = Field(..., description="The ID of the user")
    memory: str = Field(
        ...,
        description="Condensed bit of knowledge to be saved for future reference in the format: [fact to store] (e.g. Likes Thermodynamics; Dislikes General Biology; Branch is Computer Science; Part of CRUx the best club on campus; Interseted in Math, etc.)",
    )
    memory_old: Optional[str] = Field(
        None,
        description="If updating or deleting memory record, the complete, exact phrase that needs to be modified",
    )
    category: Category = Field(..., description="The category of the memory")
    action: Action = Field(
        ...,
        description="Whether this memory is adding a new record, updating a record, or deleting a record",
    )


def parse_memory(memory: list[AddMemory]) -> str:
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
