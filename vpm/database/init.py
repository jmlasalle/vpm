from sqlmodel import SQLModel
from sqlalchemy import text
import os
from pathlib import Path
from .config import engine
from ..config import settings

def create_home_trigger():
    """Create trigger to ensure only one row exists in the home table."""
    trigger_sql = """
    CREATE TRIGGER single_row_check
        BEFORE INSERT ON home
        WHEN (SELECT COUNT(*) FROM home) >= 1
        BEGIN
            SELECT RAISE(ABORT, 'Only one row allowed in home table. Use update to update home information.');
        END;
    """
    try:
        with engine.connect() as connection:
            connection.execute(text(trigger_sql))
            connection.commit()
    except Exception as e:
        raise

def init_db(overwrite: bool = False) -> str:
    """Initialize the database and create all tables.
    
    Args:
        overwrite: Whether to overwrite existing database
        
    Returns:
        Database URL
    """
    db_path = settings.get_database_path()
    
    if db_path.exists() and overwrite:
        db_path.unlink()
    
    if db_path.exists() and not overwrite:
        raise FileExistsError(
            f'Database already exists at {db_path}. To overwrite include `--overwrite`'
        )
    
    # Ensure app directory exists
    settings.ensure_data_directory()
    
    # Create tables
    SQLModel.metadata.create_all(engine)
    
    # Create triggers
    create_home_trigger()
    
    return str(db_path) 