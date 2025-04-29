# imports
from sqlmodel import Field, SQLModel, Relationship
import uuid
from decimal import Decimal
from pydantic_extra_types.currency_code import Currency
from datetime import datetime, date, timezone
from dateutil.rrule import rrule, MONTHLY, YEARLY
import enum


# classes
class BaseModel(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(
        default=datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now()},
    )

@enum.unique
class equipType(enum.StrEnum):
    oven = "Oven"
    range = "Range"
    stove = "Stove"
    microwave = " Microwave"
    dishwasher = "Dishwasher"
    fridge = "Refredgerator"
    freezer = "Freezer"
    garbage_disposal = "Garbage Disposal"

# tables
class Home(BaseModel, table=True):
    name: str = Field(unique=True)
    address: str
    rooms: list["Room"] | None = Relationship(back_populates="home", cascade_delete=True)
    equipment: list["Equipment"] | None = Relationship(back_populates="home", cascade_delete=True)
    tasks: list["Task"] = Relationship(back_populates="home", cascade_delete=True)


class Room(BaseModel, table=True):
    home_id: uuid.UUID = Field(foreign_key="home.id")
    home: Home = Relationship(back_populates="rooms")
    equipment: list["Equipment"] | None = Relationship(back_populates="room", cascade_delete=True)

class Equipment(BaseModel, table=True):
    equip_type: equipType
    room_id: uuid.UUID = Field(foreign_key="room.id")
    room: Room = Relationship(back_populates="equipment")
    home_id: uuid.UUID = Field(foreign_key="home.id")
    home: Home = Relationship(back_populates="equipment")
    tasks: list["Task"] | None = Relationship(back_populates="equipment", cascade_delete=True)
    brand: str | None
    model: str | None
    model_number: int | None
    manual_url: str | None
    manuf_url: str | None
    serial_num: str | None
    install_date: date | None
    remove_date: date | None
    cost: Decimal | None = Field(decimal_places=2)
    currency: Currency | None = Field(default="USD")

class TaskTemplate(BaseModel, table=True):
    equip_type: equipType
    frequency: str
    interval: int
    description: str
    tasks: list["Task"] = Relationship(back_populates="template")

class Task(BaseModel, table=True):
    template_id: uuid.UUID = Field(foreign_key="tasktemplate.id")
    template: TaskTemplate = Relationship(back_populates="tasks")
    equipment_id: uuid.UUID = Field(foreign_key="equipment.id")
    equipment: Equipment = Relationship(back_populates="tasks")
    home_id: uuid.UUID = Field(foreign_key="home.id")
    home: Home = Relationship(back_populates="tasks")
    description: str | None
    date_due: date
    date_complete: date | None
    complete: bool = Field(default= False)
