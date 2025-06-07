from sqlmodel import Field, Relationship
from .base import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
import uuid
from .elements import Element
from .parts import Part

class TaskType(BaseModel):
    """Base type for maintenance tasks."""
    interval: int | None = None
    interval_unit: str | None = None
    link: Optional[str] = Field(default=None, nullable=True)

class Task(TaskType, table=True):
    """Model representing a maintenance task."""
    element_id: uuid.UUID = Field(foreign_key="element.id")
    element: Element = Relationship(back_populates="tasks")
    date_due: Optional[datetime] = Field(default=None, nullable=True)
    date_complete: Optional[datetime] = Field(default=None, nullable=True)
    complete: bool = Field(default=False)
    cost_parts: Optional[Decimal] = Field(default=None, nullable=True) 
    cost_labor: Optional[Decimal] = Field(default=None, nullable=True)
    # Optional relationship to Parts (no cascade delete since Parts belong to Elements)
    parts: Optional[List[Part]] = Relationship(back_populates="task", default=None, nullable=True) 