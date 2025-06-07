from sqlmodel import Field, Relationship
from .base import BaseModel
from typing import Optional
from .documents import Document

class Contact(BaseModel, table=True):
    """Model representing a contact."""
    email: str = Field(unique=True, nullable=False)
    phone: Optional[str] = Field(default=None)
    company: Optional[str] = None
    street: Optional[str] = None
    postal_box: Optional[str] = None
    town: Optional[str] = None
    state_region: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    documents: Optional[Document] = Relationship(back_populates="contact", cascade_delete=True)