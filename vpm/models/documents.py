from sqlmodel import Field, Relationship
from .base import BaseModel
from typing import Optional, List, TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from .property import Home, Room
    from .elements import Element, ElementType
    from .parts import Part, PartType
    from .tasks import Task, TaskType

class Document(BaseModel, table=True):
    """Model representing a document."""
    doc_type: Optional[str] = Field(default=None, nullable=True)
    file_name: Optional[str] = Field(default=None, nullable=True)
    home_id: Optional[uuid.UUID] = Field(default=None, nullable=True)
    home: Optional["Home"] = Relationship(back_populates="documents")
    room_id: Optional[uuid.UUID] = Field(foreign_key="room.id", default=None, nullable=True)
    room: Optional["Room"] = Relationship(back_populates="documents")
    element_type_id: List[Optional[uuid.UUID]] = Field(foreign_key="elementtype.id", default=None, nullable=True)
    element_types: List[Optional["ElementType"]] = Relationship(back_populates="documents") 
    element_id: Optional[uuid.UUID] = Field(foreign_key="element.id", default=None, nullable=True)
    element: Optional["Element"] = Relationship(back_populates="documents")
    part_type_id: List[Optional[uuid.UUID]] = Field(foreign_key="parttype.id", default=None, nullable=True)
    part_types: List[Optional["PartType"]] = Relationship(back_populates="documents")
    part_id: Optional[uuid.UUID] = Field(foreign_key="part.id", default=None, nullable=True)
    parts: Optional[List["Part"]] = Relationship(back_populates="documents")
    task_type_id: List[Optional[uuid.UUID]] = Field(foreign_key="tasktype.id", default=None, nullable=True)
    task_types: List[Optional["TaskType"]] = Relationship(back_populates="documents")
    task_id: Optional[uuid.UUID] = Field(foreign_key="task.id", default=None, nullable=True)
    task: Optional["Task"] = Relationship(back_populates="documents")
