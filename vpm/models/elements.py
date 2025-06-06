from sqlmodel import Field, Relationship
from .base import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
import uuid

class ElementType(BaseModel):
    """Base type for equipment elements."""
    brand: Optional[str] = None
    model: Optional[str] = None
    model_number: Optional[int] = None
    manual_url: Optional[str] = None
    manufacture_url: Optional[str] = None
    cost: Optional[Decimal] = Field(decimal_places=2)
    currency: Optional[str] = Field(default="USD")

class Element(ElementType, table=True):
    """Model representing an equipment element."""
    equip_type: str
    # room_id: uuid.UUID = Field(foreign_key="room.id")
    # room: Room = Relationship(back_populates="elements")
    tasks: List["Task"] = Relationship(back_populates="element", cascade_delete=True)
    serial_num: Optional[str] = None
    install_date: Optional[datetime] = None
    remove_date: Optional[datetime] = None

class TaskType(BaseModel):
    """Base type for maintenance tasks."""
    interval: int | None = None
    interval_unit: str | None = None
    link: Optional[str] = None

class Task(TaskType, table=True):
    """Model representing a maintenance task."""
    element_id: Optional[uuid.UUID] = Field(foreign_key="element.id")
    element: Element = Relationship(back_populates="tasks")
    date_due: Optional[datetime] = None
    date_complete: Optional[datetime] = None
    complete: bool = Field(default=False)
    cost: Optional[Decimal] = None 