from sqlmodel import Session, select
from decimal import Decimal
import json, uuid, csv
from datetime import datetime, date, timezone
from dateutil.rrule import rrule, YEARLY, MONTHLY, WEEKLY, DAILY

from .database import *
from .models import *

# Add Functions
def add_item(model):
    with Session(engine) as session:
        session.add(model)
        session.commit()
        session.refresh(model)
        return model

def add_home(name: str, address: str):
    m = addItem(Home(name=name, address=address))
    return m

def add_room(name: str, home_id: uuid.UUID):
    m = addItem(Room(name=name, home_id=home_id))
    return m

def add_element(name: str, equip_type: str, room_id: uuid.UUID):
    with Session(engine) as session:
        home_id = session.exec(select(Room).where(Room.id == room_id)).one().home_id
    m = addItem(Element(name=name, equip_type=equip_type.lower(), room_id=room_id, home_id=home_id, install_date=None))
    t = addTask(m.id)
    return m

def add_task_type(
    equip_type: str,
    frequency: str,
    interval: int,
    description: str = None,
    link: str = None):
    tt = addItem(TaskType(name=name, equip_type=equip_type.lower(), frequency=frequency, interval=interval, description=description, link=link))
    return tt

def add_task(element_id: uuid.UUID, name: str, description: str, date_due: datetime) -> Task:
    element = getElement(element_id = element_id)
    task = addItem(Task(name = name, element_id = element_id, home_id = element.home_id, description = description, date_due = date_due))
    return task


def add_task_from_template(element_id: uuid.UUID):
    element = getElement(element_id = element_id)
    templates = getTaskType(equip_type = element.equip_type)
    tasks = list()
    for tt in templates:
        task = addItem(Task(
            name = tt.name,
            template_id = tt.id,
            element_id = element.id,
            home_id = element.home_id,
            description = tt.description,
            date_due = nextDate(freq=tt.frequency, interval=tt.interval)))
        tasks.append(task)
    return tasks

# ---- Get Functions ----
def getHome(home_id: uuid.UUID = None, name:str = None):
    with Session(engine) as session:
        if home_id:
            h = session.exec(select(Home).where(Home.id == home_id)).one()
            return h
        elif name:
            h = session.exec(select(Home).where(Home.name == name)).one()
            return h
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

def getElement(element_id: uuid.UUID = None, room_id: uuid.UUID = None, home_id: uuid.UUID = None):
    with Session(engine) as session:
        if element_id:
            r = session.exec(select(Element).where(Element.id == element_id)).one()
            return r
        elif room_id:
            r = session.exec(select(Element).where(Element.room_id == room_id)).all()
            return r
        elif home_id:
            r = session.exec(select(Element).where(Element.home_id == home_id)).all()
            return r
        else:
            r = session.exec(select(Element)).all()
            return r

def getTaskType(tt_id: uuid.UUID = None, equip_type:str = None):
    with Session(engine) as session:
        if tt_id:
            t = session.exec(select(TaskType).where(TaskType.id == tt_id)).one()
            return (t)
        elif equip_type:
            t = session.exec(select(TaskType).where(TaskType.equip_type == equip_type)).all()
            return (t)
        else:
            r = session.exec(select(TaskType)).all()
            return r

def getTask(task_id: uuid.UUID = None, element_id: uuid.UUID = None, room_id: uuid.UUID = None, home_id: uuid.UUID = None):
    with Session(engine) as session:
        if task_id:
            r = session.exec(select(Task).where(Task.id == task_id)).one()
            return r
        elif element_id:
            r = session.exec(select(Task).where(Task.equipmen_id == element_id)).all()
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

def serialize(obj) -> str:
    try:
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        else:
            return str(obj)
    except:
        raise TypeError("Object cannot be converted to stringN")

# ---- DB Functions ----
def addTaskTypes(path: str = "./data/task-templates.csv"):
    l = 0
    with open(path) as f:
        for t in csv.DictReader(f):
            tt = addItem(TaskType(
                name= t["name"],
                equip_type = t['equip_type'],
                frequency = t['frequency'],
                interval = t['interval'],
                description = t['description'],
                link = t['link']
                ))
            l += 1
    return l

def addDemoHome():
    h = addHome(name="Demo Home", address="145 Testing Way")
    r1 = addRoom(name="Kitchen", home_id=h.id)
    r2 = addRoom(name="Mechanical Closet", home_id=h.id)
    r3 = addRoom(name="Bathroom", home_id=h.id)
    e1 = addElement(name="Fridge", equip_type="refrigerator", room_id=r1.id)
    e2 = addElement(name="Stove", equip_type="stove", room_id=r1.id)
    e3 = addElement(name="Dishwasher",equip_type="dishwasher", room_id=r1.id)
    e4 = addElement(name="Water Heater",equip_type="water heater - tank", room_id=r2.id)
    e5 = addElement(name="Heat Pump", equip_type="heat pump - ducted", room_id=r2.id)

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