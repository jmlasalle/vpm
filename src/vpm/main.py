from sqlmodel import Session, select
from decimal import Decimal
import json, uuid, csv
from datetime import datetime, date, timezone
from dateutil.rrule import rrule, YEARLY, MONTHLY, WEEKLY, DAILY

from .database import *
from .models import *

# Add Functions
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

def addHome(name: str, address: str):
    m = addItem(Home(name=name, address=address))
    return m

def addRoom(name: str, home_id: uuid.UUID):
    m = addItem(Room(name=name, home_id=home_id))
    return m

def addEquipment(name: str, equip_type: str, room_id: uuid.UUID):
    with Session(engine) as session:
        home_id = session.exec(select(Room).where(Room.id == room_id)).one().home_id
    m = addItem(Equipment(name=name, equip_type=equip_type.lower(), room_id=room_id, home_id=home_id, install_date=None))
    t = addTask(m.id)
    print(t)
    return m

def addTaskTemplate(
    equip_type: str,
    frequency: str,
    interval: int,
    description: str = None,
    link: str = None):
    if equip_type in equipTypes:
        print(f'{equip_type} is valid')
    tt = addItem(TaskTemplate(name=name, equip_type=equip_type.lower(), frequency=frequency, interval=interval, description=description, link=link))
    return tt

def addTask(equipment_id: uuid.UUID):
    equipment = getEquipment(equipment_id = equipment_id)
    templates = getTaskTemplate(equip_type = equipment.equip_type)
    tasks = list()
    for tt in templates:
        task = addItem(Task(
            name = tt.name,
            template_id = tt.id,
            equipment_id = equipment.id,
            home_id = equipment.home_id,
            description = tt.description,
            date_due = nextDate(freq=tt.frequency, interval=tt.interval)))
        tasks.append(task)
    return tasks

# ---- Get Functions ----
def getHome(home_id: uuid.UUID = None, name:str = None):
    with Session(engine) as session:
        if home_id:
            h = session.exec(select(Home).where(Home.id == home_id)).one()
            return (h, h.rooms, h.equipment)
        elif name:
            h = session.exec(select(Home).where(Home.name == name)).one()
            return (h, h.rooms, h.equipment)
        else:
            r = session.exec(select(Home)).all()
            return r

def getRoom(room_id: uuid.UUID = None, home_id: uuid.UUID = None):
    with Session(engine) as session:
        if room_id: 
            r = session.exec(select(Room).where(Room.id == room_id)).one()
            return r
        elif home_id:
            r = session.exec(select(Room).where(Room.home_id == home_id)).all()
            return r
        else:
            r = session.exec(select(Room)).all()
            return r

def getEquipment(equipment_id: uuid.UUID = None, room_id: uuid.UUID = None, home_id: uuid.UUID = None):
    with Session(engine) as session:
        if equipment_id:
            r = session.exec(select(Equipment).where(Equipment.id == equipment_id)).one()
            return r
        elif room_id:
            r = session.exec(select(Equipment).where(Equipment.room_id == room_id)).all()
            return r
        elif home_id:
            r = session.exec(select(Equipment).where(Equipment.home_id == home_id)).all()
            return r
        else:
            r = session.exec(select(Equipment)).all()
            return r

def getTaskTemplate(tt_id: uuid.UUID = None, equip_type:str = None):
    with Session(engine) as session:
        if tt_id:
            t = session.exec(select(TaskTemplate).where(TaskTemplate.id == tt_id)).one()
            return (t)
        elif equip_type:
            t = session.exec(select(TaskTemplate).where(TaskTemplate.equip_type == equip_type)).all()
            return (t)
        else:
            r = session.exec(select(TaskTemplate)).all()
            return r

def getTask(task_id: uuid.UUID = None, equipment_id: uuid.UUID = None, room_id: uuid.UUID = None, home_id: uuid.UUID = None):
    with Session(engine) as session:
        if task_id:
            r = session.exec(select(Task).where(Task.id == task_id)).one()
            return r
        elif equipment_id:
            r = session.exec(select(Task).where(Task.equipmen_id == equipment_id)).all()
            return r
        elif room_id:
            r = session.exec(select(Task).where(Task.room_id == room_id)).all()
            return r
        elif home_id:
            r = session.exec(select(Task).where(Task.home_id == home_id)).all()
            return r
        else:
            r = session.exec(select(Task)).all()
            return r

# ---- Update Function -----
def updateItem(table:str, id: uuid.UUID, **kwargs):
    with Session(engine) as session:
        r = session.exec(select(eval(table.capitalize())).where(eval(f'{table.capitalize()}.id') == id)).one()
        r.sqlmodel_update(kwargs)
        session.add(r)
        session.commit()
        session.refresh(r)
        return r

# ---- Delete Functions ----
def deleteItem(table: str, id: uuid.UUID):
    with Session(engine) as session:
        r = session.exec(select(eval(table.capitalize())).where(eval(f'{table.capitalize()}.id') == id)).one()
        session.delete(r)
        session.commit()

# ---- Utility Functions ----
def nextDate(freq: str, interval: int, dt: datetime = datetime.today()):
    if freq.upper() in ["YEARLY", "MONTHLY", "WEEKLY", "DAILY"]:
        return rrule(freq=eval(freq.upper()), interval=interval, dtstart=dt)[1]
    else:
        raise TypeError(f'{freq.upper()} must be one of YEARLY, MONTHLY, WEEKLY, DAILY')

# ---- DB Functions ----
def addTaskTemplates(path: str = "./data/task-templates.csv"):
    with open(path) as f:
        for t in csv.DictReader(f):
            addItem(TaskTemplate(
                name= t["name"],
                equip_type = t['equip_type'],
                frequency = t['frequency'],
                interval = t['interval'],
                description = t['description'],
                link = t['link']
                ))

def getSchemas():
    inspector = inspect(engine)
    return inspector.get_schema_names()

def getTables():
    inspector = inspect(engine)
    schemas = inspector.get_schema_names()
    t = list()
    for schema in schemas:
        for table_name in inspector.get_table_names(schema=schema):
            t.append(table_name)
    return t

def getCols(table: str, schema: str = "main"):
    inspector = inspect(engine)
    schemas = inspector.get_schema_names()
    try: 
        schema in schemas
        try: 
            table in getTables()
            cols = list()
            for c in inspector.get_columns(table, schema):
                cols.append(c["name"])
            return cols
        except:
            ValueError(f'{table} is not a valid {engine.url} table. Run getTables() for list of valid tables.')
    except:
        ValueError(f'{schema} is not a valid {engine.url} schema. Run getSchemas() for list of valid schemas.')