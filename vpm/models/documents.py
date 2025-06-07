from sqlmodel import Field
from .base import BaseModel
from typing import Optional

class Document(BaseModel, table=True):
    """Model representing a document."""
    doc_type: Optional[str] = Field(default=None, nullable=True)
    file_name: Optional[str] = Field(default=None, nullable=True) 