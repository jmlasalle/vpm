# imports
from sqlmodel import Field, SQLModel, Relationship
import uuid
from decimal import Decimal
from datetime import datetime



# classes
class Home(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True)
    address: str
    rooms: list["Room"] | None = Relationship(back_populates="home", cascade_delete=True)
    created_at: datetime = Field(default=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )

class Room(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    home_id: uuid.UUID = Field(foreign_key="home.id")
    home: Home = Relationship(back_populates="rooms")
    equipments: list["Equipment"] | None = Relationship(back_populates="room", cascade_delete=True)
    created_at: datetime = Field(default=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )

class Equipment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    equip_type: str 
    room_id: uuid.UUID = Field(foreign_key="room.id")
    room: Room = Relationship(back_populates="equipments")
    brand: str | None
    model: str | None
    model_number: int | None
    manual_url: str | None
    manuf_url: str | None
    serial_num: str | None
    install_date: datetime | None
    remove_date: datetime | None
    cost: Decimal | None = Field(decimal_places=2)
    created_at: datetime = Field(default=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )