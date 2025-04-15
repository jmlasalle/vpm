# imports
from sqlmodel import SQLModel, create_engine

# create db
sqlite_file_name = "./vpm-db.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    return sqlite_url
