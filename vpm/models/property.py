from sqlmodel import Field, Relationship
from .base import BaseModel
from typing import List, Optional
import uuid

class Home(BaseModel, table=True):
    """Model representing a home property."""
    address: str
    rooms: List["Room"] = Relationship(back_populates="home", cascade_delete=True)

class Room(BaseModel, table=True):
    """Model representing a room in a home."""
    level: int = Field(default=0)
    home_id: uuid.UUID = Field(foreign_key="home.id")
    home: Home = Relationship(back_populates="rooms")
    elements: List["Element"] = Relationship(back_populates="room", cascade_delete=True) 