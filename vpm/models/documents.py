from sqlmodel import Field, Relationship
from .base import BaseModel
from typing import Optional, TYPE_CHECKING
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
    path: Optional[str] = Field(default=None, nullable=True)
    url: Optional[str] = Field(default=None, nullable=True)
    
    # Home relationship
    home_id: Optional[uuid.UUID] = Field(foreign_key="home.id", default=None, nullable=True)
    home: Optional["Home"] = Relationship(back_populates="documents")
    
    # Element relationships
    element_id: Optional[uuid.UUID] = Field(foreign_key="element.id", default=None, nullable=True)
    element: Optional["Element"] = Relationship(back_populates="documents")
