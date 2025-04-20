# imports
import typer
from typing_extensions import Annotated
from rich import print
from sqlmodel import Session, select
from decimal import Decimal
import json, uuid, csv
from datetime import datetime, date, timezone

from .database import create_db_and_tables, engine
from .models import Home, Room, Equipment, equipType
from .utils import addItem

# create Typer app
app = typer.Typer(no_args_is_help=True)

# init commands
@app.command()
def version():
    """Prints the application's version number."""
    print("Version 0.01")

@app.command()
def create_db():
    """Initializes the database and creates all necessary tables."""
    db_url = create_db_and_tables()
    print(db_url)

@app.command()
def db():
    """Prints the database engine configuration (including URL)."""
    print(engine)

@app.command()
def add_demo_home():
    """Adds a predefined set of demo data (Home, Rooms, Equipment).

    Useful for quickly populating the database for testing or demonstration.
    """
    h = add_home(name="Demo Home 2", address="145 Testing Way")
    print(h)
    r1 = add_room(name="Kitchen", home_id=h)
    r2 = add_room(name="Mechanical Closet", home_id=h)
    r3 = add_room(name="Bathroom", home_id=h)
    add_equipment(name="Fridge", equip_type="refrigerator", room_id=r1.id)
    add_equipment(name="Stove", equip_type="stove", room_id=r1.id)
    add_equipment(name="Dishwasher",equip_type="dishwasher", room_id=r1)
    add_equipment(name="Water Heater",equip_type="water heater", room_id=r2)
    add_equipment(name="Heat Pump", equip_type="heat pump", room_id=r2)


# Add commands
@app.command()
def add_home(name: str, address: str):
    """Adds a new Home record to the database.

    Args:
        name: The name for the new home.
        address: The street address for the new home.
    """
    m = addItem(Home(name=name, address=address))
    print(m)

@app.command()
def add_room(name: str, home_id: uuid.UUID):
    """Adds a new Room record associated with a specific Home.

    Args:
        name: The name for the new room (e.g., 'Kitchen', 'Bedroom').
        home_id: The UUID of the Home this room belongs to.
    """
    m = addItem(Room(name=name, home_id=home_id))
    print(m)

@app.command()
def add_equipment(name: str, equip_type: equipType, room_id: uuid.UUID):
    """Adds a new Equipment record associated with a specific Room.

    Args:
        name: The name for the new equipment (e.g., 'Main Fridge').
        equip_type: The type of equipment (e.g., 'refrigerator', 'heat pump').
        room_id: The UUID of the Room where this equipment is located.
    """
    with Session(engine) as session:
        home_id = session.exec(select(Room).where(Room.id == room_id)).one().home_id
    m = addItem(Equipment(name=name, equip_type=equip_type, room_id=room_id, home_id=home_id))
    print(m)

# get item commands
@app.command()
def get_home(home_id: Annotated[uuid.UUID, typer.Option()] = None):
    """Retrieves and prints Home records.

    If --home-id is provided, retrieves a single Home by its UUID.
    Otherwise, retrieves and prints all Home records.
    """
    with Session(engine) as session:
        if home_id:
            h = session.exec(select(Home).where(Home.id == home_id)).one()
            print(h)
            print(h.rooms)
            print(h.equipment)
        else:
            r = session.exec(select(Home)).all()
            print(r)

@app.command()
def get_room(
    room_id: Annotated[uuid.UUID, typer.Option()] = None, 
    home_id: Annotated[uuid.UUID, typer.Option()] = None
    ):
    """Retrieves and prints Room records.

    Can filter by:
    - --room-id: Retrieves a single Room by its UUID.
    - --home-id: Retrieves all Rooms belonging to the specified Home UUID.
    If no options are provided, retrieves all Room records.
    """
    with Session(engine) as session:
        if room_id: 
            r = session.exec(select(Room).where(Room.id == room_id)).one()
            print(r)
            print(r.equipment)
        elif home_id:
            r = session.exec(select(Room).where(Room.home_id == home_id)).all()
            print(r)
        else:
            r = session.exec(select(Room)).all()
            print(r)

@app.command()
def get_equipment(
    equipment_id: Annotated[uuid.UUID, typer.Option()] = None, 
    room_id: Annotated[uuid.UUID, typer.Option()] = None, 
    home_id: Annotated[uuid.UUID, typer.Option()] = None
    ):
    """Retrieves and prints Equipment records.

    Can filter by:
    - --equipment-id: Retrieves a single piece of Equipment by its UUID.
    - --room-id: Retrieves all Equipment belonging to the specified Room UUID.
    - --home-id: Retrieves all Equipment located in any Room within the specified Home UUID.
    If no options are provided, retrieves all Equipment records.
    """
    with Session(engine) as session:
        if equipment_id:
            print("option 1")
            r = session.exec(select(Equipment).where(Equipment.id == equipment_id)).one()
            print(r)
        elif room_id:
            print("option 2")
            r = session.exec(select(Equipment).where(Equipment.room_id == room_id)).all()
            print(r)
        elif home_id:
            print("option 3")
            result = session.exec(select(Equipment))
            for r in result:
                l = []
                if r.room.home_id == home_id:
                    l.append(r)
                print(l)
        else:
            print("option 4")
            r = session.exec(select(Equipment)).all()
            print(r)

# update commands
@app.command()
def update_home(
    home_id: uuid.UUID, 
    name: Annotated[str | None, typer.Option()] = None, 
    address: Annotated[str | None, typer.Option()] = None):
    """Updates the name and/or address of an existing Home.

    Args:
        home_id: The UUID of the Home record to update.
        name: The optional new name to set for the Home.
        address: The optional new address to set for the Home.
    """
    with Session(engine) as session:
        r = session.exec(select(Home).where(Home.id == home_id)).one()
        if name:
            r.name = name
        if address:
            r.address = address
        session.add(r)
        session.commit()
        session.refresh(r)
        print(r)

@app.command()
def update_room(
    room_id: uuid.UUID, 
    name: Annotated[str | None, typer.Option()] = None
    ):
    """Updates the name of an existing Room.

    Args:
        room_id: The UUID of the Room record to update.
        name: The optional new name to set for the Room.
    """
    with Session(engine) as session:
        r = session.exec(select(Room).where(Room.id == room_id)).one()
        if name:
            r.name = name
        session.add(r)
        session.commit()
        session.refresh(r)
        print(r)

@app.command()
def update_equipment(
    equipment_id: uuid.UUID,
    name: Annotated[str | None, typer.Option()] = None,
    equip_type: Annotated[str | None, typer.Option()] = None,
    brand: Annotated[str | None, typer.Option()] = None,
    model: Annotated[str | None, typer.Option()] = None,
    model_number: Annotated[str | None, typer.Option()] = None,
    manual_url: Annotated[str | None, typer.Option()] = None,
    manuf_url: Annotated[str | None, typer.Option()] = None,
    serial_num: Annotated[str | None, typer.Option()] = None,
    install_date: Annotated[str | None, typer.Option()] = None,
    remove_date: Annotated[str | None, typer.Option()] = None,
    cost: Annotated[float  | None, typer.Option()] = None\
    ):
    """Updates attributes of an existing piece of Equipment.

    Args:
        equipment_id: The UUID of the Equipment record to update.
        name: Optional new name.
        equip_type: Optional new equipment type.
        brand: Optional brand name.
        model: Optional model identifier.
        model_number: Optional model number.
        manual_url: Optional URL for the manual.
        manuf_url: Optional URL for the manufacturer.
        serial_num: Optional serial number.
        install_date: Optional installation date.
        remove_date: Optional removal date.
        cost: Optional purchase cost.
    """
    with Session(engine) as session:
        r = session.exec(select(Equipment).where(Equipment.id == equipment_id)).one()
        if name:
            r.name = name
        if equip_type: 
            r.equip_type = equip_type
        if brand: 
            r.brand = brand
        if model: 
            r.model = model
        if model_number: 
            r.model_number = model_number
        if manual_url: 
            r.manual_url = manual_url
        if serial_num: 
            r.serial_num = serial_num
        if install_date: 
            r.install_date = date.fromisoformat(install_date)
            print(f'install_date: {r.install_date}')
        if remove_date: 
            r.remove_date = date.fromisoformat(remove_date)
        if cost: 
            r.cost = cost
            session.add(r)
        session.commit()
        session.refresh(r)
        print(r)

#delete commands
@app.command()
def delete_home(home_id: uuid.UUID):
    """Deletes a Home record and potentially associated Rooms/Equipment (depending on cascades).

    Args:
        home_id: The UUID of the Home record to delete.
    """
    with Session(engine) as session:
        r = session.exec(select(Home).where(Home.id == home_id)).one()
        session.delete(r)
        session.commit()
        # confirm delete
        rr = session.exec(select(Home).where(Home.id == home_id)).one()
        if rr is None:
            print(f'Home deleted: {r}')

@app.command()
def delete_room(room_id: uuid.UUID):
    """Deletes a Room record. Associated Equipment might also be affected depending on database setup.

    Args:
        room_id: The UUID of the Room record to delete.
    """
    with Session(engine) as session:
        r = session.exec(select(Room).where(Room.id == room_id)).one()
        session.delete(r)
        session.commit()
        # confirm delete
        rr = session.exec(select(Room).where(Room.id == room_id)).one()
        if rr is None:
            print(f'Room deleted: {r}')

@app.command()
def delete_equipment(equipment_id: uuid.UUID):
    """Deletes an Equipment record.

    Args:
        equipment_id: The UUID of the Equipment record to delete.
    """
    with Session(engine) as session:
        r = session.exec(select(Equipment).where(Equipment.id == equipment_id)).one()
        session.delete(r)
        session.commit()
        # confirm delete
        rr = session.exec(select(Equipment).where(Equipment.id == equipment_id)).one()
        if rr is None:
            print(f'Equipment deleted: {r}')

# Onboarding
@app.command()
def Onboard():
    print("Welcome to vpm!")
    #create home
    print("Lets start by setting up your home.")
    hname = typer.prompt("What name do you want to call your home?")
    haddress = typer.prompt(f'What is the street address for {hname}?')
    h = add_home(hname, haddress)
    print(f'Now lets add your first room.')
    add_more_rooms = "y"
    while add_more_rooms == "y":
            rname = typer.prompt("Room name:")
            r = add_room(rname, h.id)
            add_more_rooms = typer.prompt("Do you want to add another room(y/n)?")
            # add_more_equip = "y"
            # print(f'What equipment does {rname} have?')
            # while add_more_equip == "y"
            #     ename = typer.prompt("what nickname do you want for the first equipment:")
            #     add_equipment(name = room_id=r.id)
            #     add_more_equip = typer.prompt("Is there more equipment in the room to add (y/n)?")

@app.command()
def dashboard(home_id: uuid.UUID):
    with Session(engine) as session:
        results = session.exec(select(Home).where(Home.id == uuid.UUID(home_id))).one()
        rooms = [r for r in h.rooms]
        print(h)
        print(rooms)