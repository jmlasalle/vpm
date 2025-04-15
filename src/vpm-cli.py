# imports
import typer
from typing_extensions import Annotated
from rich import print
from sqlmodel import Session, select
import json, uuid, csv

from .database import create_db_and_tables, engine
from .models import Home, Room, Equipment, EquipmentTemplate

# create Typer app
app = typer.Typer(no_args_is_help=True)

# init commands
@app.command()
def create_db():
    db_url = create_db_and_tables()
    #create demo home
    print(db_url)

@app.command()
def build_template_tables():
    equip_path = "./equipment-templates.csv"
    with open(equip_path,'r') as data:
        for t in csv.DictReader(data):
            print(t['equip_type'])
            add_equipment_template(
                equip_type=t['equip_type'],
                brand=t['brand'],
                model=t['model'],
                model_number=t['model_number'],
                manual_url=t['manual_url'],
                manuf_url=t['manuf_url'],
                lifespan=t['lifespan']
            )


@app.command()
def add_demo_home():
    h = add_home(name="Demo Home 7", address="145 Testing Way")
    r1 = add_room(name="Kitchen", home_id=h)
    r2 = add_room(name="Mechanical Closet", home_id=h)
    r3 = add_room(name="Bathroom", home_id=h)
    add_equipment(name="Fridge", template_id=get_equipment_template(uuid.UUID("d5d5ec6a08e54869a7c06112413c7104")).id, room_id=r1.id)
    add_equipment(name="Stove", template_id="16ea436a86cb4ab8805d1392b2e55ad2", room_id=r1.id)
    add_equipment(name="Dishwasher", template_id="3681189c265b405a9e88bfab6539b2ff", room_id=r1.id)
    add_equipment(name="Water Heater", template_id="cd305469bcc74fe0830416893c527a0e", room_id=r2.id)
    add_equipment(name="Heat Pump", template_id="bc7faae417c64b20bad16c65a126e6e7", room_id=r2.id)


# Home commands
@app.command()
def add_home(name: str, address: str):
    with Session(engine) as session:
        new_home = Home(name=name, address=address)
        session.add(new_home)
        session.commit()
        session.refresh(new_home)
        print(new_home)
        return new_home

@app.command()
def get_homes():
    with Session(engine) as session:
        statement = select(Home)
        results = session.exec(statement)
        for h in results:
            print(h)

@app.command()
def get_home(home_id: uuid.UUID):
    with Session(engine) as session:
        statement = select(Home).where(Home.id == uuid.UUID(home_id))
        results = session.exec(statement)
        h = results.one()
        print(h)

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
def update_home(home_id: uuid.UUID, name: Annotated[str | None, typer.Option()] = None, address: Annotated[str | None, typer.Option()] = None):
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
def add_room(name: str, home_id: uuid.UUID):
    with Session(engine) as session:
        new_room = Room(name=name, home=home_id)
        session.add(new_room)
        session.commit()
        session.refresh(new_room)
        print(new_room)
        return new_room

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

# Equipment Template commands
@app.command()
def add_equipment_template(
    equip_type: str,
    brand: Annotated[str | None, typer.Option()] = None,
    model: Annotated[str | None, typer.Option()] = None,
    model_number: Annotated[str | None, typer.Option()] = None,
    manual_url: Annotated[str | None, typer.Option()] = None,
    manuf_url: Annotated[str | None, typer.Option()] = None,
    lifespan: Annotated[str | None, typer.Option()] = None
):
    with Session(engine) as session:
        new_equip_template = EquipmentTemplate(equip_type=equip_type, brand=brand, model=model, model_number=model_number, manual_url=manual_url, manuf_url=manuf_url, lifespan=lifespan)
        session.add(new_equip_template)
        session.commit()
        session.refresh(new_equip_template)
        print(new_equip_template)
        return new_equip_template

@app.command()
def get_equipment_templates():
    with Session(engine) as session:
        statement = select(EquipmentTemplate)
        result = session.exec(statement)
        for r in result:
            print(r)

@app.command()
def get_equipment_template(equipment_template_id: uuid.UUID):
    with Session(engine) as session:
        statement = select(EquipmentTemplate).where(EquipmentTemplate.id == equipment_template_id)
        result = session.exec(statement)
        et = result.one()
        print(et)
        return et

@app.command()
def update_equipment_template():
    None

@app.command()
def delete_equipment_template(template_id: uuid.UUID):
    with Session(engine) as session:
        statement = select(EquipmentTemplate).where(EquipmentTemplate.id == template_id)
        results = session.exec(statement)
        et = results.one()
        session.delete(et)
        session.commit()

        statement = select(EquipmentTemplate).where(EquipmentTemplate.id == template_id)
        results = session.exec(statement)
        et = results.one()

        if et is None:
            print(f'Room deleted: {template_id}')

# Equipment commands
@app.command()
def add_equipment(template_id: uuid.UUID, room_id: uuid.UUID, name: Annotated[str, typer.Option()] = None):
    with Session(engine) as session:
        new_equipment = Equipment(name=name, template_id=template_id, room=room_id )
        # get equipment template
        template = session.select(EquipmentTemplate).where(EquipmentTemplate.equip_type == equip_type)
        # get template tasks
        # create task instances
        session.add(new_eqipment)
        session.commit()

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

# run application
if __name__ == "__main__":

    app()