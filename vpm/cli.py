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
from typing import Optional
from uuid import UUID
from .services.property import HomeService, RoomService
from .services.elements import ElementService, TaskService
from .services.database import DatabaseService
from .services.demo import DemoService
from .models.property import Home, Room
from .models.elements import Element, Task
from .models.parts import Part
from .models.contacts import Contact
from .models.documents import Document
from .database import init_db, create_home_trigger, create_db_and_tables, engine
from .models import *
from .core import *
import vpm.home
import vpm.room
import vpm.elements
import vpm.tasks
import vpm.parts
import vpm.db

APP_NAME = "vpm-cli"
VERSION = "0.01"

# create Typer app
app = typer.Typer(no_args_is_help=True)

# Add subcommands
app.add_typer(vpm.home.app, name="home")
app.add_typer(vpm.room.app, name="room")
app.add_typer(vpm.elements.app, name="element")
app.add_typer(vpm.tasks.app, name="task")
app.add_typer(vpm.parts.app, name="part")
app.add_typer(vpm.db.app, name="db")

# Initialize services
home_service = HomeService()
room_service = RoomService()
element_service = ElementService()
task_service = TaskService()
database_service = DatabaseService()
demo_service = DemoService()

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
def dashboard(home_id: uuid.UUID):
    """Display a dashboard view of a home and its rooms"""
    with Session(engine) as session:
        results = session.exec(select(Home).where(Home.id == uuid.UUID(home_id))).one()
        rooms = [r for r in h.rooms]
        print(h)
        print(rooms)

@app.command()
def onboard():
    """Interactive onboarding process to set up your first home"""
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
        print(f'What element does {rname} have?')
        while add_more_equip.lower() == "y":
            ename = typer.prompt("what nickname do you want for the element")
            etype = typer.prompt(f'What is {ename}\'s element type?')
            edate = typer.prompt(f'What date was {ename} installed (YYYY-MM-DD)')
            add_element(room_id=r.id, name=ename, equip_type=etype, install_date=datetime.strptime(edate, '%Y-%m-%d'))
            add_more_equip = typer.prompt(f'Are there more elements in {rname} to add (y/n)?')
        add_more_rooms = typer.prompt("Do you want to add another room(y/n)?")

if __name__ == "__main__":
    app()