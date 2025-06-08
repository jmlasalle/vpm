import typer
from typing import Optional
from typing_extensions import Annotated
from uuid import UUID
from .services.property import RoomService
from .services.elements import ElementService
from .models.property import Room
from .models.elements import Element

app = typer.Typer(no_args_is_help=True)
room_service = RoomService()
element_service = ElementService()

@app.command()
def add(
    name: Annotated[str, typer.Option(prompt="Room name")]
    ):
    room = add_room(name=name)
    print(room)

@app.command()
def get(
    name: Annotated[str, typer.Option(prompt="Name")]
    ) -> None:
    room = get_item(table="room", name=name)
    print(room)

@app.command()
def update_room(
    name: Annotated[str, typer.Option(prompt="Room Name")] = None
    ):
    args = {k: v for k, v in locals().items() if v is not None}
    r = update_item(
        table="Room", 
        id=element_id,
        **args
        )
    print(r)

@app.command()
def delete_room(name: Annotated[str, typer.Option(prompt="Room name")]) -> None:
    delete_item(table="Room", name=name)

if __name__ == "__main__":
    app()