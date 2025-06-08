from sqlmodel import Field, Relationship
from .base import BaseModel
from typing import TYPE_CHECKING
from decimal import Decimal
from datetime import datetime
from uuid import UUID
from pydantic import field_validator
from ..utils.helpers import validate_task_category, validate_interval_unit, validate_currency

if TYPE_CHECKING:
    from .elements import Element
    from .parts import Part

class TaskType(BaseModel):
    """Base type for maintenance tasks."""
    task_category: str | None = Field(default=None, nullable=True)
    interval: int | None = None
    interval_unit: str | None = None
    link: str | None= Field(default=None, nullable=True)

    @field_validator("task_category")
    def validate_task_category(cls, v):
        return validate_task_category(v)

    @field_validator("interval_unit")
    def validate_interval_unit(cls, v):
        return validate_interval_unit(v)

class Task(TaskType, table=True):
    """Model representing a maintenance task."""
    element_id: UUID = Field(foreign_key="element.id")
    element: "Element" = Relationship(back_populates="tasks")
    date_due: datetime | None = Field(default=None, nullable=True)
    date_complete: datetime | None = Field(default=None, nullable=True)
    complete: bool = Field(default=False)
    cost_parts: Decimal | None = Field(default=None, nullable=True) 
    cost_labor: Decimal | None = Field(default=None, nullable=True)
    currency: str | None = Field(default=None, nullable=True)
    # Optional relationship to Parts (no cascade delete since Parts belong to Elements)
    parts: list["Part"] = Relationship(back_populates="task")

    @field_validator("currency")
    def validate_currency(cls, v):
        return validate_currency(v)
