import typer
from typing_extensions import Annotated
from rich import print
from .database.init import init_db
from .database.config import engine

app = typer.Typer(no_args_is_help=True)

@app.command()
def create(overwrite: Annotated[bool, typer.Option("--overwrite", prompt="Overwrite existing DB?")] = False):
    """Initializes the database and creates all necessary tables."""
    try:
        db_url = init_db(overwrite=overwrite)
        print(db_url)
    except FileExistsError as e:
        print(e)

@app.command()
def info():
    """Prints the database engine configuration (including URL)."""
    print(engine)

if __name__ == "__main__":
    app() 