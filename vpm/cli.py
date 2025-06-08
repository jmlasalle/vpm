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
from .database.config import engine
from .services.property import HomeService, RoomService
from .services.elements import ElementService, TaskService
from .services.database import DatabaseService
from .models.property import Home, Room
from .models.elements import Element
from .models.tasks import Task
from .models.parts import Part
from .models.contacts import Contact
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

if __name__ == "__main__":
    app()