from sqlmodel import Session, select
from .database import engine
from .models import Home, Room, Equipment

# Internal Functions
def addItem(model):
    """Adds a SQLModel instance to the database session and commits it.

    This is a general utility function to handle adding new records
    to the database.

    Args:
        model: The SQLModel instance (e.g., Home, Room, Equipment) to add.

    Returns:
        The added and refreshed SQLModel instance with updated fields (like ID).
    """
    with Session(engine) as session:
        session.add(model)
        session.commit()
        session.refresh(model)
        return model