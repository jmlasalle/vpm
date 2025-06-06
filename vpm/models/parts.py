from sqlmodel import Field
from .base import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
import uuid

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
    task_id: uuid.UUID = Field(foreign_key="task.id") 