from typing import Optional
import typer
from uuid import UUID
from .services.elements import ElementService
from .models.elements import Element, ElementType
from .utils.logging import logger
from typing_extensions import Annotated
from rich import print
import json
from datetime import datetime

app = typer.Typer(no_args_is_help=True)
element_service = ElementService()

def serialize(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, UUID):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

@app.command(help="Adds a new element to the local database.")
def add(
    name: Annotated[str, typer.Option(prompt="Element name")],
    type: Annotated[ElementType, typer.Option(prompt="Element type")],
    description: Annotated[str, typer.Option(prompt="Description")]
) -> None:
    try:
        element = element_service.add_element(name=name, type=type, description=description)
        print(json.dumps(element.model_dump(), indent=4, default=serialize))
    except Exception as e:
        print(f"Error: {str(e)}")

@app.command(help="Get element information")
def get(
    name: Annotated[str, typer.Option(prompt="Element name")]
) -> None:
    element = element_service.get_element(name=name)
    print(json.dumps(element.model_dump(), indent=4, default=serialize))

@app.command(help="Update element information")
def update(
    name: Annotated[str, typer.Option(prompt="Element name")],
    new_name: Annotated[str | None, typer.Option()] = None,
    type: Annotated[ElementType | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None
) -> None:
    element = element_service.get_element(name=name)
    args = {k: v for k, v in locals().items() if v is not None and k != 'name'}
    result = element_service.update_element(element_id=element.id, **args)
    print(json.dumps(result.model_dump(), indent=4, default=serialize))

@app.command(help="Delete an element")
def delete(
    name: Annotated[str, typer.Option(prompt="Element name")]
) -> None:
    try:
        element = element_service.get_element(name=name)
        element_service.delete_element(element_id=element.id)
        print(f'Element "{name}" deleted successfully')
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    app() 