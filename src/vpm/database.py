# imports
from sqlmodel import SQLModel, create_engine
from sqlalchemy import inspect
import os

# create db
sqlite_file_name = "./data/vpm.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables(db_path: str = sqlite_file_name, overwrite: bool = False):
    if os.path.isfile(db_path) and overwrite == True:
        os.remove(db_path)
        SQLModel.metadata.create_all(engine)
        return sqlite_url
    elif os.path.isfile(db_path):
        raise FileExistsError(f'FileExistsError: Database already exists at {db_path}. To overwrite include `--overwrite`')
    else:
        SQLModel.metadata.create_all(engine)
        return sqlite_url
        