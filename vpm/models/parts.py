from sqlmodel import Field, Relationship
from .base import BaseModel
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal
from datetime import datetime
import uuid


if TYPE_CHECKING:
    from .tasks import Task
    from .elements import Element, ElementType
    from .documents import Document

class PartType(BaseModel):
    """Base type for parts."""
    brand: Optional[str] = None
    model: Optional[str] = None
    model_number: Optional[str] = None
    cost: Optional[Decimal] = None
    currency: Optional[str] = None
    element_type_id: Optional[uuid.UUID] = Field(foreign_key="elementtype.id", default=None, nullable=True)
    element_type: Optional["ElementType"] = Relationship(back_populates="part_types")
    documents: Optional[List["Document"]] = Relationship(back_populates="part", cascade_delete=True)

class Part(PartType, table=True):
    """Model representing a part."""
    serial_num: Optional[str] = None
    install_date: Optional[datetime] = None
    remove_date: Optional[datetime] = None
    # Primary relationship to Element
    element_id: uuid.UUID = Field(foreign_key="element.id", nullable=False)
    element: "Element" = Relationship(back_populates="parts")
    # Optional relationship to Task
    task_id: Optional[uuid.UUID] = Field(foreign_key="task.id", nullable=True)
    task: Optional["Task"] = Relationship(back_populates="parts")