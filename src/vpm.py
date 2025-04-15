# imports
import typer
from rich import print
from sqlmodel import Session, select
from uuid import uuid4
import json

from .database import create_db_and_tables, engine
from .models import Home, Room, Equipment

# create Typer app
app = typer.Typer(no_args_is_help=True)

# commands
@app.command()
def create_db():
    db_url = create_db_and_tables()
    #create demo home
    print(db_url)

@app.command()
def create_demo_home():
    with Session(engine) as session:
        home_id = str(uuid4())
        room_id1 = str(uuid4())
        room_id2 = str(uuid4())
        equip_id1 = str(uuid4())
        equip_id2 = str(uuid4())
        equip_id3 = str(uuid4())
        equip_id4 = str(uuid4())
        new_home = Home(id=home_id, name="Demo Home", address="123 Testing Way")
        new_room1 = Room(id=room_id1, name="Kitchen", home_id=home_id)
        new_room2 = Room(id=room_id2, name="Bathroom", home_id=home_id)
        new_equipment1 = Equipment(id=equip_id1, equip_type="Stove", room_id=room_id1)
        new_equipment2 = Equipment(id=equip_id2, equip_type="Refridgerator", room_id=room_id1)
        new_equipment3 = Equipment(id=equip_id3, equip_type="Water Heater", room_id=room_id2)
        new_equipment4 = Equipment(id=equip_id4, equip_type="Sink", room_id=room_id2)
        session.add(new_home)
        session.add(new_room1)
        session.add(new_room2)
        session.add(new_equipment1)
        session.add(new_equipment2)
        session.add(new_equipment3)
        session.add(new_equipment4)
        session.commit()
    session.close()

# create commands
@app.command()
def create_home(name: str, address: str):
    with Session(engine) as session:
        new_home = Home(id= str(uuid4()),name=name, address=address)
        session.add(new_home)
        session.commit()
    session.close()

@app.command()
def create_room(name: str, home_name: str):
    with Session(engine) as session:
        statement = select(Home).where(Home.name == home_name)
        # print(statement)
        results = session.exec(statement)
        home_id = results.first().id
        print(home_id)
        new_room = Room(id= str(uuid4()),name=name, home=home_id)
        session.add(new_room)
        session.commit()
    session.close()

@app.command()
def create_equipment(name: str, room_id: str):
    with Session(engine) as session:
        new_equipment = Equipment(id= str(uuid4()),name=name, room=room_id)
        # get equipment template
        # get template tasks
        # create task instances
        session.add(new_eqipment)
        session.commit()
    session.close()

# get commands
@app.command()
def get_homes():
    with Session(engine) as session:
        statement = select(Home)
        results = session.exec(statement)
        for r in results:
            print(f'{r.name}: {r.address}')

@app.command()
def get_home(name: str):
    with Session(engine) as session:
        statement = select(Home).where(Home.name == name)
        results = session.exec(statement)
        # print(json.dumps(results))
        for r in results:
            print(f'Name: {r.name}\nAddress: {r.address}\nRooms:')
            for i in r.rooms:
                print(f'{i}\nEquipment:')
                for e in i.equipments:
                    print(f'{e}')

@app.command()
def get_rooms(home_id: str):
    with Session(engine) as session:
        statement = select(Home).where(Home.id == home_id)
        result = session.exec(statement)
        r = result.one()
        for room in r.rooms:
            print(room.equipments)

# run application
if __name__ == "__main__":

    app()