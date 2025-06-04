# imports
from sqlmodel import Field, SQLModel, Relationship
from typing import Annotated, Union, Literal
import uuid
from decimal import Decimal
from pydantic import AfterValidator
from datetime import datetime, timezone
from dateutil.rrule import rrule, MONTHLY, YEARLY
import enum

# ---- validators ----
equipTypes = Union[Literal[
    "oven",
    "range",
    "stove",
    "microwave",
    "dishwasher",
    "refrigerator",
    "freezer",
    "garbage disposal",
    "water heater – tank",
    "water heater – tankless",
    "heat pump – ducted"
    ]]


powerSource = Union[Literal["electric", "gas", "wood", "propane", "diesel", "solar"]]
   
# ---- classes -----
class BaseModel(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(
        default=datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now()},
    )

## ---- tables -----
class Home(BaseModel, table=True):
    name: str = Field(unique=True)
    address: str
    rooms: list["Room"] | None = Relationship(back_populates="home", cascade_delete=True)
    element: list["Element"] | None = Relationship(back_populates="home", cascade_delete=True)
    tasks: list["Task"] = Relationship(back_populates="home", cascade_delete=True)


class Room(BaseModel, table=True):
    home_id: uuid.UUID = Field(foreign_key="home.id")
    home: Home = Relationship(back_populates="rooms")
    element: list["Element"] | None = Relationship(back_populates="room", cascade_delete=True)

class ElementType(BaseModel, table=True):
    brand: str | None
    model: str | None
    model_number: int | None
    manual_url: str | None
    manufacture_url: str | None
    cost: Decimal | None = Field(decimal_places=2)
    currency: str| None = Field(default=None)


class Element(ElementType, table=True):
    equip_type: str
    room_id: uuid.UUID = Field(foreign_key="room.id")
    room: Room = Relationship(back_populates="element")
    home_id: uuid.UUID = Field(foreign_key="home.id")
    home: Home = Relationship(back_populates="element")
    tasks: list["Task"] | None = Relationship(back_populates="element", cascade_delete=True)
    serial_num: str | None
    install_date: datetime | None
    remove_date: datetime | None
    cost: Decimal | None = Field(decimal_places=2)
    currency: str | None = Field(default=None)

class TaskType(BaseModel, table=True):
    description: str | None
    interval: int
    interval_unit: str
    link: str | None
    equip_type: equipTypes


class Task(TaskType, table=True):
    element_id: uuid.UUID | None = Field(foreign_key="element.id")
    element: Element = Relationship(back_populates="tasks")
    home_id: uuid.UUID = Field(foreign_key="home.id")
    home: Home = Relationship(back_populates="tasks")
    description: str | None
    date_due: datetime | None
    date_complete: datetime | None
    complete: bool = Field(default= False)
    cost: Decimal | None

class PartType(BaseModel, table=True):
    brand: str | None
    model: str | None
    model_number: str | None
    cost: Decimal | None

class Part(PartType, table=True):
    serial_num: str | None
    install_date: datetime | None
    remove_date: datetime | None
    task_id: uuid.UUID = Field(foreign_key="task.id")
    task