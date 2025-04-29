from sqlmodel import Session, select
from .database import engine
from .models import Home, Room, Equipment, TaskTemplate, Task, equipType
from datetime import datetime, date, timezone

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

def next_date(freq: str, interval: int, dt: datetime = datetime.today()):
    if freq.upper() in ["YEARLY", "MONTHLY", "WEEKLY", "DAILY"]:
        return rrule(freq=eval(freq.upper()), interval=interval, dtstart=dt)[1]
    else:
        raise TypeError(f'{freq.upper()} must be one of YEARLY, MONTHLY, WEEKLY, DAILY')
