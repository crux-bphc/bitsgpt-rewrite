from datetime import datetime
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


class LongTermMemory(BaseModel):
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


class ShortTermMemory(BaseModel):
    id: str = Field(
        ...,
        title="User ID",
        description="Unique identifier for the user.",
        examples=["123"],
    )
    message_id: str = Field(
        ...,
        title="Message ID",
        description="Unique identifier for the message.",
        examples=["8b47dfe8-0960-4b80-b551-471b47a650a0"],
    )
    created_at: datetime = Field(
        ...,
        title="Created At",
        description="Timestamp of when the memory was created.",
        examples=["2022-01-01T00:00:00"],
    )
    query: str = Field(
        ...,
        title="Query",
        description="User query.",
        examples=["Where is the library?"],
    )
    reply: str = Field(
        ...,
        title="Reply",
        description="Agent's reply.",
        examples=["The library is on the second floor."],
    )
    agent: str = Field(
        ...,
        title="Agent",
        description="Agent that replied.",
        examples=["INTENT_CLASSIFIER_AGENT"],
    )
