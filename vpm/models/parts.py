from sqlmodel import Field, Relationship
from .base import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
import uuid
from .tasks import Task
from .elements import Element

class PartType(BaseModel):
    """Base type for parts."""
    brand: Optional[str] = None
    model: Optional[str] = None
    model_number: Optional[str] = None
    cost: Optional[Decimal] = None

class Part(PartType, table=True):
    """Model representing a part."""
    serial_num: Optional[str] = None
    install_date: Optional[datetime] = None
    remove_date: Optional[datetime] = None
    # Primary relationship to Element
    element_id: uuid.UUID = Field(foreign_key="element.id", nullable=False)
    element: Element = Relationship(back_populates="parts")
    # Optional relationship to Task
    task_id: Optional[uuid.UUID] = Field(foreign_key="task.id", nullable=True)
    task: Optional[Task] = Relationship(back_populates="parts")