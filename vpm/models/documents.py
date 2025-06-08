from sqlmodel import Field, Relationship
from .base import BaseModel
from typing import Optional, TYPE_CHECKING
import uuid
from pydantic import field_validator
from .picklist import DocumentCategory
from ..utils.helpers import validate_url

if TYPE_CHECKING:
    from .property import Home, Room
    from .elements import Element
    from .parts import Part
    from .tasks import Task
    from .contacts import Contact

class Document(BaseModel, table=True):
    """Model representing a document."""
    document_category: Optional[str] = Field(default=None, nullable=True)
    file_name: Optional[str] = Field(default=None, nullable=True)
    path: Optional[str] = Field(default=None, nullable=True)
    url: Optional[str] = Field(default=None, nullable=True)
    
    # Home relationship
    home_id: Optional[uuid.UUID] = Field(foreign_key="home.id", default=None, nullable=True)
    home: Optional["Home"] = Relationship(back_populates="documents")
    
    # Element relationships
    element_id: Optional[uuid.UUID] = Field(foreign_key="element.id", default=None, nullable=True)
    element: Optional["Element"] = Relationship(back_populates="documents")

    # Contact relationship
    contact_id: Optional[uuid.UUID] = Field(foreign_key="contact.id", default=None, nullable=True)
    contact: Optional["Contact"] = Relationship(back_populates="documents")

    @field_validator("document_category")
    def validate_document_category(cls, v):
        if v not in DocumentCategory:
            raise ValueError(f"Invalid document category: {v}")
        return v
    
    @field_validator("url")
    def validate_url(cls, v):
        return validate_url(v)
