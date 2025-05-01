# imports
from sqlmodel import Field, SQLModel, Relationship
from typing import Annotated
import uuid
from decimal import Decimal
from pydantic import AfterValidator
from pydantic_extra_types.currency_code import Currency
from datetime import datetime, date, timezone
from dateutil.rrule import rrule, MONTHLY, YEARLY
import enum

# ---- validators ----
equipTypes = [
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
    "heat pump – ducted",
    ]

def EquipType(val):
    if val in equipTypes:
        return val
    else:
        raise ValueError(f'{val} is not a valid equipment type. Call equipTypes for list of valid equipment types.')

def powerSource(val):
    s = ["electric", "gas", "wood", "propane", "diesel", "solar"]
    if val:
        if val in s:
            return val
        else:
            raise ValueError(f'{val} is not a valid power source. Must be one of {s}')
    else:
        return val

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
    equipment: list["Equipment"] | None = Relationship(back_populates="home", cascade_delete=True)
    tasks: list["Task"] = Relationship(back_populates="home", cascade_delete=True)


class Room(BaseModel, table=True):
    home_id: uuid.UUID = Field(foreign_key="home.id")
    home: Home = Relationship(back_populates="rooms")
    equipment: list["Equipment"] | None = Relationship(back_populates="room", cascade_delete=True)

class Equipment(BaseModel, table=True):
    equip_type: Annotated[str, AfterValidator(EquipType)]
    room_id: uuid.UUID = Field(foreign_key="room.id")
    room: Room = Relationship(back_populates="equipment")
    home_id: uuid.UUID = Field(foreign_key="home.id")
    home: Home = Relationship(back_populates="equipment")
    tasks: list["Task"] | None = Relationship(back_populates="equipment", cascade_delete=True)
    brand: str | None
    model: str | None
    model_number: int | None
    power_source: Annotated[str | None, AfterValidator(powerSource)]
    manual_url: str | None
    manuf_url: str | None
    serial_num: str | None
    install_date: date | None
    remove_date: date | None
    cost: Decimal | None = Field(decimal_places=2)
    currency: Currency | None = Field(default="USD")

class TaskTemplate(BaseModel, table=True):
    equip_type: Annotated[str, AfterValidator(EquipType)]
    frequency: str
    interval: int
    description: str | None
    link: str | None
    tasks: list["Task"] | None = Relationship(back_populates="template")

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