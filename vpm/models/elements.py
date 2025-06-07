from sqlmodel import Field, Relationship
from .base import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
import uuid
from .tasks import Task
from .parts import Part

class ElementType(BaseModel):
    """Base type for equipment elements."""
    brand: Optional[str] = Field(default=None, nullable=True)
    model: Optional[str] = Field(default=None, nullable=True)
    model_number: Optional[int] = Field(default=None, nullable=True)
    manual_url: Optional[str] = Field(default=None, nullable=True)
    manufacture_url: Optional[str] = None
    cost: Optional[Decimal] = Field(decimal_places=2)
    currency: Optional[str] = Field(default="USD")

class Element(ElementType, table=True):
    """Model representing an equipment element."""
    room_id: uuid.UUID = Field(foreign_key="room.id")
    room: Room = Relationship(back_populates="elements")
    tasks: Optional[List[Task]] = Relationship(back_populates="element", cascade_delete=True, default=None, nullable=True)
    parts: Optional[List[Part]] = Relationship(back_populates="element", cascade_delete=True, default=None, nullable=True)
    serial_num: Optional[str] = Field(default=None, nullable=True)
    install_date: Optional[datetime] = Field(default=None, nullable=True)
    remove_date: Optional[datetime] = Field(default=None, nullable=True)