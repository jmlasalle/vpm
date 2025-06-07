from sqlmodel import Field, Relationship
from .base import BaseModel
from typing import TYPE_CHECKING
from decimal import Decimal
from datetime import datetime
from uuid import UUID


if TYPE_CHECKING:
    from .tasks import Task
    from .parts import Part
    from .documents import Document
    from .property import Room

class ElementType(BaseModel):
    """Base type for equipment elements."""
    brand: str | None = Field(default=None, nullable=True)
    model: str | None = Field(default=None, nullable=True)
    model_number: int | None = Field(default=None, nullable=True)
    manual_url: str | None = Field(default=None, nullable=True)
    manufacture_url: str | None = None
    cost: Decimal | None = Field(decimal_places=2)
    currency: str | None = Field(default="USD")

class Element(ElementType, table=True):
    """Model representing an equipment element."""
    serial_num: str | None = Field(default=None, nullable=True)
    install_date: datetime | None = Field(default=None, nullable=True)
    remove_date: datetime | None = Field(default=None, nullable=True)
    room_id: UUID = Field(foreign_key="room.id")
    room: "Room" = Relationship(back_populates="elements")
    tasks: list["Task"] = Relationship(back_populates="elements", cascade_delete=True)
    parts: list["Part"] = Relationship(back_populates="elements", cascade_delete=True)
    documents: list["Document"] = Relationship(back_populates="elements", cascade_delete=True)
