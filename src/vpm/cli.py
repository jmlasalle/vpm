# imports
import typer
from typing_extensions import Annotated
from rich import print
from sqlmodel import Session, select
from decimal import Decimal
import json, uuid, csv, os
from datetime import datetime, timezone
from dateutil.rrule import rrule, YEARLY, MONTHLY, WEEKLY, DAILY
from pathlib import Path

from .database import create_db_and_tables, engine
from .models import *
from .core import *
import src.vpm.home

APP_NAME = "vpm-cli"
VERSION = "0.01"

# create Typer app
app = typer.Typer(no_args_is_help=True)
app.add_typer(src.vpm.home.app, name="home")

# init commands
@app.callback(invoke_without_command=True)
def config():
    """Creates config file if it doesn't exists. Runs before every command"""
    app_dir = typer.get_app_dir(APP_NAME)
    config_path: Path = Path(app_dir) / "config.json"
    if not os.path.exists(app_dir):
        os.mkdir(app_dir)
    if not config_path.is_file():
        config = {
            "app_name":APP_NAME,
            "version": VERSION,
            "username": "",
            "subscribed": "False",
            "token": ""}
        json_object = json.dumps(config, indent=4)
        config_path.write_text(json_object)

@app.command()
def version():
    """Prints the application's version number."""
    print(f'Version {VERSION}')

@app.command()
def create_db(overwrite: Annotated[bool, typer.Option("--overwrite", prompt="Overwrite existing DB?")] = False):
    """Initializes the database and creates all necessary tables."""
    try:
        db_url = create_db_and_tables(db_path=sqlite_file_name, overwrite=overwrite)
        print(db_url)
    except FileExistsError as e:
        print(e)
    
@app.command()
def db():
    """Prints the database engine configuration (including URL)."""
    print(engine)

# Add commands
@app.command()
def add_home(
    name: Annotated[str, typer.Option(prompt="Unique name")], 
    address: Annotated[str, typer.Option(prompt="Street address")]
    ):
    home = addHome(name=name, address=address)
    print(json.dumps(home.model_dump(), default=serialize))

@app.command()
def add_room(
    home_id: Annotated[uuid.UUID, typer.Option(prompt="Home ID")],
    name: Annotated[str, typer.Option(prompt="Room name")]
    ):
    room = addRoom(name=name, home_id=home_id)
    print(room)

@app.command()
def add_element(
    room_id: Annotated[uuid.UUID, typer.Option(prompt="Room ID")],
    name: Annotated[str, typer.Option(prompt="Element name")], 
    equip_type: Annotated[str, typer.Option(prompt="Element type")],
    install_date: Annotated[datetime, typer.Option(prompt="Installation date")] = None
    ):
    with Session(engine) as session:
        home_id = session.exec(select(Room).where(Room.id == room_id)).one().home_id
    element = addElement(name=name, equip_type=equip_type.lower(), room_id=room_id, home_id=home_id, install_date=install_date)
    print(element)

@app.command()
def add_task(
    element_id: Annotated[uuid.UUID, typer.Option(prompt="ID for the element the taks is link to")],
    name: Annotated[str, typer.Option(prompt="Task name")],
    description: Annotated[str | None, typer.Option(prompt="Task description")],
    date_due: Annotated[str | None, typer.Option(prompt="Due date in YYYY-MM-DD format")] = None
    ):
    task = addTask(element_id=element_id, name=name, description=description, date_due=datetime.strptime(date_due, '%Y-%m-%d'))
    print(task)

# get item commands
@app.command()
def get_home(
    home_id: Annotated[uuid.UUID, typer.Option(prompt="Home ID")] = None, 
    name: Annotated[str, typer.Option(prompt="Home name")] = None
    ) -> dict:
    h = getHome(home_id, name)
    print(h)

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
    r = getRoom(room_id, home_id)
    print(r)

@app.command()
def get_element(
    element_id: Annotated[uuid.UUID, typer.Option()] = None, 
    room_id: Annotated[uuid.UUID, typer.Option()] = None, 
    home_id: Annotated[uuid.UUID, typer.Option()] = None
    ):
    """Retrieves and prints Element records.

    Can filter by:
    - --element-id: Retrieves a single piece of Element by its UUID.
    - --room-id: Retrieves all Element belonging to the specified Room UUID.
    - --home-id: Retrieves all Element located in any Room within the specified Home UUID.
    If no options are provided, retrieves all Element records.
    """
    e = getElement(element_id, room_id, home_id)
    print(e)

@app.command()
def getTaskTemplate(
    tt_id: Annotated[uuid.UUID, typer.Option()] = None, 
    equip_type:Annotated[str, typer.Option()] = None):
    tt = getTaskTemplate(tt_id=tt_id, equip_type=equip_type)
    print(tt)

@app.command()
def get_task(
    task_id: Annotated[uuid.UUID, typer.Option()] = None, 
    element_id: Annotated[uuid.UUID, typer.Option()] = None, 
    room_id: Annotated[uuid.UUID, typer.Option()] = None, 
    home_id: Annotated[uuid.UUID, typer.Option()] = None):
    t = getTask(task_id, element_id, room_id, home_id)
    print(t)

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
    args = {k: v for k, v in locals().items() if v is not None}
    r = updateItem(
        table="Home", 
        id=element_id,
        **args
        )
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
    args = {k: v for k, v in locals().items() if v is not None}
    r = updateItem(
        table="Room", 
        id=element_id,
        **args
        )
    print(r)

@app.command()
def update_element(
    element_id: uuid.UUID,
    name: Annotated[str, typer.Option()] = None,
    equip_type: Annotated[str, typer.Option()] = None,
    brand: Annotated[str, typer.Option()] = None,
    model: Annotated[str, typer.Option()] = None,
    model_number: Annotated[str, typer.Option()] = None,
    power_source: Annotated[str, typer.Option()] = None,
    manual_url: Annotated[str, typer.Option()] = None,
    manuf_url: Annotated[str, typer.Option()] = None,
    serial_num: Annotated[str, typer.Option()] = None,
    install_date: Annotated[str, typer.Option()] = None,
    remove_date: Annotated[str, typer.Option()] = None,
    cost: Annotated[float , typer.Option()] = None
    ):
    """Updates attributes of an existing piece of Element.

    Args:
        element_id: The UUID of the Element record to update.
        name: Optional new name.
        equip_type: Optional new element type.
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
    args = {k: v for k, v in locals().items() if v is not None}
    r = updateItem(
        table="Element", 
        id=element_id,
        **args
        )
    print(r)

@app.command()
def update_task(
    task_id: Annotated[uuid.UUID, typer.Option()],
    name: Annotated[str, typer.Option()] = None,
    description: Annotated[str, typer.Option()] = None,
    date_due: Annotated[datetime, typer.Option()] = None,
    date_complete: Annotated[datetime, typer.Option()] = None,
    complete: Annotated[bool, typer.Option()] = None):
    args = {k: v for k, v in locals().items() if v is not None}
    r = updateItem(
        table="Task", 
        id=element_id,
        **args
        )
    print(j)

# ---- delete commands ----
@app.command()
def delete_home(home_id: Annotated[uuid.UUID, typer.Option(prompt="Home ID")]) -> None:
    deleteItem(table="Home", id=home_id)

@app.command()
def delete_room(room_id: Annotated[uuid.UUID, typer.Option(prompt="Room ID")]) -> None:
    deleteItem(table="Room", id=room_id)

@app.command()
def delete_element(element_id: Annotated[uuid.UUID, typer.Option(prompt="Element ID")]) -> None:
    deleteItem(table="Element", id=element_id)

@app.command()
def delete_task(element_id: Annotated[uuid.UUID, typer.Option(prompt="Task ID")]) -> None:
    deleteItem(table="Task", id=task_id)

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
    while add_more_rooms.lower() == "y":
        rname = typer.prompt("Room name")
        r = add_room(home_id=h.id, name=rname)
        add_more_equip = "y"
        print(f'What elment does {rname} have?')
        while add_more_equip.lower() == "y":
            ename = typer.prompt("what nickname do you want for the element")
            etype = typer.prompt(f'What is {ename}\'s element type?')
            edate = typer.prompt(f'What date was {ename} installed (YYYY-MM-DD)')
            add_element(room_id=r.id, name = ename, equip_type=etype, install_date=datetime.strptime(edate, '%Y-%m-%d'))
            add_more_equip = typer.prompt(f'Are there more elements in {rname} to add (y/n)?')
        add_more_rooms = typer.prompt("Do you want to add another room(y/n)?")
            

@app.command()
def dashboard(home_id: uuid.UUID):
    with Session(engine) as session:
        results = session.exec(select(Home).where(Home.id == uuid.UUID(home_id))).one()
        rooms = [r for r in h.rooms]
        print(h)
        print(rooms)

if __name__ == "__main__":
    app()