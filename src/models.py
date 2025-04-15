# imports
from sqlmodel import Field, SQLModel, Relationship
import uuid

# classes
class Home(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True)
    address: str
    rooms: list["Room"] | None = Relationship(back_populates="home")

class Room(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    home_id: uuid.UUID = Field(foreign_key="home.id")
    home: Home = Relationship(back_populates="rooms")
    equipments: list["Equipment"] | None = Relationship(back_populates="room")

class EquipmentTemplate(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    equip_type: str = Field(unique=True)
    brand: str | None
    model: str | None
    model_number: int | None
    manual_url: str | None
    manuf_url: str | None
    lifespan: int | None
    equipments: list["Equipment"] | None = Relationship(back_populates="template")

class Equipment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str | None
    room_id: uuid.UUID = Field(foreign_key="room.id")
    room: Room = Relationship(back_populates="equipments")
    template_id: uuid.UUID = Field(foreign_key="equipmenttemplate.id")
    template: EquipmentTemplate = Relationship(back_populates="equipments")
    serial_num: str | None
    install_date: str | None
    remove_date: str | None
    manual_url: str | None