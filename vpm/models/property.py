from sqlmodel import Field, Relationship
from .base import BaseModel
from typing import List, Optional

class Home(BaseModel, table=True):
    """Model representing a home property."""
    address: str

class Room(BaseModel, table=True):
    """Model representing a room in a home."""
    level: int = Field(default=0)
    elements: List["Element"] = Relationship(back_populates="room", cascade_delete=True) 