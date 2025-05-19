import typer
from typing_extensions import Annotated
import json, uuid
from datetime import datetime

from .core import *

app = typer.Typer(no_args_is_help=True)

@app.command(help="Adds a new home to the local database.")
def add(
    name: Annotated[str, typer.Option(prompt="Unique name")], 
    address: Annotated[str, typer.Option(prompt="Street address")]
    ) -> None:
    home = addHome(name=name, address=address)
    print(json.dumps(home.model_dump(), indent=4, default=serialize))

@app.command(help="Gets all homes, or a specific home if --home-id or --name is given.")
def get(
    home_id: Annotated[uuid.UUID | None, typer.Option(help="Home ID")] = None, 
    name: Annotated[str | None, typer.Option(help="Home name")] = None) -> None:
    if all:
        home = getHome()
        print(json.dumps(home.model_dump(), indent=4, default=serialize))
    else:
        home = getHome(home_id, name)
        print(home)
    

@app.command()
def update(
    home_id: uuid.UUID, 
    name: Annotated[str | None, typer.Option()] = None, 
    address: Annotated[str | None, typer.Option()] = None) -> None:
    args = {k: v for k, v in locals().items() if v is not None}
    r = updateItem(
        table="Home", 
        id=element_id,
        **args
        )
    print(r)

@app.command()
def delete(home_id: Annotated[uuid.UUID, typer.Option(prompt="Home ID")]) -> None:
    try:
        deleteItem(table="Home", id=home_id)
        print('Home deleted')
    except exception as e:
        print(e)

if __name__ == "__main__":
    app()