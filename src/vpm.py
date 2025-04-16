# imports
import typer
from typing_extensions import Annotated
from rich import print
from sqlmodel import Session, select
import json, uuid, csv

from .database import create_db_and_tables, engine
from .models import Home, Room, Equipment

# create Typer app
app = typer.Typer(no_args_is_help=True)

# Internal Functions
def make_json(model):
    return model.json()

def addItem(model):
    with Session(engine) as session:
        session.add(model)
        session.commit()
        session.refresh(model)
        return model

# init commands
@app.command()
def create_db():
    db_url = create_db_and_tables()
    #create demo home
    print(db_url)

@app.command()
def add_demo_home():
    h = add_home(name="Demo Home 2", address="145 Testing Way")
    print(h)
    r1 = add_room(name="Kitchen", home_id=h)
    r2 = add_room(name="Mechanical Closet", home_id=h)
    r3 = add_room(name="Bathroom", home_id=h)
    add_equipment(name="Fridge", equip_type="refrigerator", room_id=r1.id)
    add_equipment(name="Stove", equip_type="stove", room_id=r1)
    add_equipment(name="Dishwasher",equip_type="dishwasher", room_id=r1)
    add_equipment(name="Water Heater",equip_type="water heater", room_id=r2)
    add_equipment(name="Heat Pump", equip_type="heat pump", room_id=r2)


# Home commands
@app.command()
def add_home(name: str, address: str):
    h = addItem(Home(name=name, address=address))
    print(h)

@app.command()
def add_room(name: str, home_id: uuid.UUID):
    r = addItem(Room(name=name, home_id=home_id))
    print(r)

@app.command()
def add_equipment(name: str, equip_type: str, room_id: uuid.UUID):
    e = addItem(Equipment(name=name, equip_type=equip_type, room_id=room_id))
    print(e)

@app.command()
def get_homes():
    with Session(engine) as session:
        results = session.exec(select(Home))
        for h in results:
            print(h.json())

@app.command()
def get_home(home_id: uuid.UUID):
    with Session(engine) as session:
        h = session.exec(select(Home).where(Home.id == home_id)).one()
        print(h.json())
        return h

@app.command()
def get_home_details(home_id: uuid.UUID):
    with Session(engine) as session:
        statement = select(Home).where(Home.id == uuid.UUID(home_id))
        results = session.exec(statement)
        h = results.one()
        rooms = [r for r in h.rooms]
        print(h)
        print(rooms)

@app.command()
def update_home(
    home_id: uuid.UUID, 
    name: Annotated[str | None, typer.Option(prompt=True)] = None, 
    address: Annotated[str | None, typer.Option(prompt=True)] = None):
    with Session(engine) as session:
        statement = select(Home).where(Home.id == home_id)
        results = session.exec(statement)
        h = results.one()
        if name:
            h.name = name
        if address:
            h.address = address
        session.add(h)
        session.commit()
        session.refresh(h)
        print(h)

@app.command()
def delete_home(home_id: uuid.UUID):
    with Session(engine) as session:
        statement = select(Home).where(Home.id == home_id)
        results = session.exec(statement)
        h = results.one()
        session.delete(h)
        session.commit()

        statement = select(Home).where(Home.id == home_id)
        results = session.exec(statement)
        h = results.one()

        if h is None:
            print(f'Home deleted: {home_id}')

# Room commands
@app.command()
def get_rooms():
    with Session(engine) as session:
        statement = select(Room)
        results = session.exec(statement)
        r = results
        for room in r:
            print(room)

@app.command()
def get_room(room_id: uuid.UUID):
    with Session(engine) as session:
        statement = select(Room).where(Room.id == room_id)
        result = session.exec(statement)
        r = result.one()
        print(r)

@app.command()
def update_room(room_id: uuid.UUID, name: Annotated[str | None, typer.Option()] = None):
    with Session(engine) as session:
        statement = select(Room).where(Room.id == room_id)
        results = session.exec(statement)
        r = results.one()
        if name:
            r.name = name
        session.add(r)
        session.commit()
        session.refresh(r)
        print(r)

@app.command()
def delete_room(room_id: uuid.UUID):
    with Session(engine) as session:
        statement = select(Room).where(Room.id == room_id)
        results = session.exec(statement)
        r = results.one()
        session.delete(r)
        session.commit()

        statement = select(Room).where(Room.id == room_id)
        results = session.exec(statement)
        r = results.one()

        if r is None:
            print(f'Room deleted: {room_id}')

# Equipment commands
@app.command()
def add_equipment(name: str, equip_type: str, room_id: uuid.UUID):
    with Session(engine) as session:
        new_equip = Equipment(name=name, equip_type=equip_type, room_id=room_id)
        session.add(new_equip)
        session.commit()
        print(new_equip)
        return new_equip

@app.command()
def get_equipments():
    None

@app.command()
def get_equipment(equipment_id):
    with Session(engine) as session:
        statement = select(Equipment).where(Equipment.id == equipment_id)
        result = session.exec(statement)
        r = result.one()
        print(r)

@app.command()
def update_equipment():
    None

@app.command()
def delete_equipment():
    None

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


# run application
if __name__ == "__main__":
    app()