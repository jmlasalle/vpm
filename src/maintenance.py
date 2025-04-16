# models
class TaskTemplate(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: str | None 
    interval: int # the interval the task is repeated on in days

class Task(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    template: str = Field(foreign_key="tasktemplate.id")
    equipment_id: str = Field(foreign_key="equipment.id")
    equipment: Equipment = Relationship(back_populates="tasks")
    due_date: str
    comeplete_date: str | None 
    name: str
    description: str | None 

class PartTemplate(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str

class Part(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    template_id: str = Field(foreign_key="parttemplate.id")

# Commands
@app.command()
def build_template_tables():
    equip_path = "./equipment-templates.csv"
    with open(equip_path,'r') as data:
        for t in csv.DictReader(data):
            print(t['equip_type'])
            add_equipment_template(
                equip_type=t['equip_type'],
                brand=t['brand'],
                model=t['model'],
                model_number=t['model_number'],
                manual_url=t['manual_url'],
                manuf_url=t['manuf_url'],
                lifespan=t['lifespan']
# Parts Template Commands
@app.command()
def add_part_template():
    None

@app.command()
def get_parts_template():
    None

@app.command()
def get_part_template():
    None

@app.command()
def update_part_template():
    None

@app.command()
def delete_part_template():
    None

# Parts Commands
def add_part():
    None

@app.command()
def get_parts():
    None

@app.command()
def get_part():
    None

@app.command()
def update_part():
    None

@app.command()
def delete_part():
    None

# Parts Template Commands
@app.command()
def add_task_template():
    None

@app.command()
def get_tasks_template():
    None

@app.command()
def get_task_template():
    None

@app.command()
def update_task_template():
    None

@app.command()
def delete_task_template():
    None

# Parts Commands
@app.command()
def add_task():
    None

@app.command()
def get_tasks():
    None

@app.command()
def get_task():
    None

@app.command()
def update_task():
    None

@app.command()
def delete_task():
    None