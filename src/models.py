# imports
from sqlmodel import Field, SQLModel, Relationship

# classes
class Home(SQLModel, table=True):
    id: str | None = Field(default=None, unique=True, primary_key=True)
    name: str = Field(unique=True)
    address: str
    rooms: list["Room"] | None = Relationship(back_populates="home")

class Room(SQLModel, table=True):
    id: str | None = Field(default=None, unique=True, primary_key=True)
    name: str
    home_id: str = Field(foreign_key="home.id")
    home: Home = Relationship(back_populates="rooms")
    equipments: list["Equipment"] | None = Relationship(back_populates="room")

class EquipmentTemplate(SQLModel, table=True):
    id: str | None = Field(default=None, unique=True, primary_key=True)
    equip_type: str
    brand: str | None
    model: str | None
    serial_num: str | None
    manual_url: str | None
    manuf_url: str | None
    lifespan: int | None

class Equipment(SQLModel, table=True):
    id: str | None = Field(default=None, unique=True, primary_key=True)
    room_id: str = Field(foreign_key="room.id")
    room: Room = Relationship(back_populates="equipments")
    tasks: list["Task"] | None = Relationship(back_populates="equipment")
    equip_type: str
    brand: str | None
    model: str | None
    serial_num: str | None
    install_date: str | None
    remove_date: str | None
    manual_url: str | None

class TaskTemplate(SQLModel, table=True):
    id: str | None = Field(default=None, unique=True, primary_key=True)
    name: str
    description: str | None 
    interval: int # the interval the task is repeated on in days

class Task(SQLModel, table=True):
    id: str | None = Field(default=None, unique=True, primary_key=True)
    template: str = Field(foreign_key="tasktemplate.id")
    equipment_id: str = Field(foreign_key="equipment.id")
    equipment: Equipment = Relationship(back_populates="tasks")
    due_date: str
    comeplete_date: str | None 
    name: str
    description: str | None 

class PartTemplate(SQLModel, table=True):
    id: str | None = Field(default=None, unique=True, primary_key=True)

class Part(SQLModel, table=True):
    id: str | None = Field(default=None, unique=True, primary_key=True)