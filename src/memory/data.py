from langchain.pydantic_v1 import BaseModel, Field
from enum import Enum
from typing import Optional


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


def parse_memory(memory: AddMemory):
    raise NotImplementedError("This function is not yet implemented")
