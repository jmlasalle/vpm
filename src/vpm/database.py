# imports
from sqlmodel import SQLModel, create_engine
from sqlalchemy import inspect

# create db
sqlite_file_name = "./data/vpm.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():
    """Creates the SQLite database file and all tables defined via SQLModel.

    This function uses the global `engine` object which points to the
    SQLite database file. It invokes SQLModel's `metadata.create_all`
    method to automatically generate the database schema based on any
    defined SQLModel classes.

    Returns:
        str: The connection URL string for the created SQLite database.
    """
    SQLModel.metadata.create_all(engine)
    return sqlite_url