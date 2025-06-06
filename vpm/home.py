from typing import Optional
import typer
from uuid import UUID
from .services.property import HomeService
from .services.elements import ElementService
from .models.property import Home
from .models.elements import Element
from .utils.logging import logger
from typing_extensions import Annotated
from rich import print
import json
from datetime import datetime

app = typer.Typer(no_args_is_help=True)
home_service = HomeService()
element_service = ElementService()

@app.command(help="Adds a new home to the local database.")
def add(
    name: Annotated[str, typer.Option(prompt="Unique name")], 
    address: Annotated[str, typer.Option(prompt="Street address")],
    description: Annotated[str, typer.Option(prompt="Description")]
    ) -> None:
    try:
        home = home_service.add_home(name=name, address=address, description=description)
        print(json.dumps(home.model_dump(), indent=4, default=serialize))
    except Exception as e:
        print("IntegrityError: A Home already exists. Use 'update' to update home information.")

@app.command(help="Get home information")
def get() -> None:
    home = home_service.get_home()
    print(json.dumps(home.model_dump(), indent=4, default=serialize))

@app.command()
def update(
    name: Annotated[str | None, typer.Option()] = None, 
    address: Annotated[str | None, typer.Option()] = None) -> None:
    home_id = home_service.get_home().id
    args = {k: v for k, v in locals().items() if v is not None}
    r = home_service.update_item(
        table="Home", 
        id=home_id,
        **args
        )
    print(r)

@app.command()
def delete() -> None:
    home_id = home_service.get_home().id
    try:
        home_service.delete_item(table="Home", id=home_id)
        print('Home deleted')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    app()