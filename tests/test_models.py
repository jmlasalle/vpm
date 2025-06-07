import pytest
from datetime import datetime
import uuid
from vpm.models import Home, Room, Element, Task, TaskType

def test_home_model():
    """Test Home model creation and validation."""
    home = Home(
        id=uuid.uuid4(),
        name="Test Home",
        address="123 Test St",
        description="A test home"
    )
    assert home.name == "Test Home"
    assert home.address == "123 Test St"
    assert home.description == "A test home"
    assert isinstance(home.id, uuid.UUID)

def test_room_model(sample_home):
    """Test Room model creation and validation."""
    room = Room(
        id=uuid.uuid4(),
        name="Test Room",
        home_id=sample_home.id,
        level=1
    )
    assert room.name == "Test Room"
    assert room.home_id == sample_home.id
    assert room.level == 1
    assert isinstance(room.id, uuid.UUID)

def test_element_model(sample_room):
    """Test Element model creation and validation."""
    element = Element(
        id=uuid.uuid4(),
        name="Test Element",
        room_id=sample_room.id,
        home_id=sample_room.home_id,
        install_date=datetime.now()
    )
    assert element.name == "Test Element"
    assert element.room_id == sample_room.id
    assert element.home_id == sample_room.home_id
    assert isinstance(element.install_date, datetime)
    assert isinstance(element.id, uuid.UUID)

def test_task_type_model():
    """Test TaskType model creation and validation."""
    task_type = TaskType(
        id=uuid.uuid4(),
        name="Test Task Type",
        frequency="monthly",
        interval=1,
        description="A test task type"
    )
    assert task_type.name == "Test Task Type"
    assert task_type.frequency == "monthly"
    assert task_type.interval == 1
    assert task_type.description == "A test task type"
    assert isinstance(task_type.id, uuid.UUID)

def test_task_model(sample_element):
    """Test Task model creation and validation."""
    due_date = datetime.now()
    task = Task(
        id=uuid.uuid4(),
        name="Test Task",
        element_id=sample_element.id,
        home_id=sample_element.home_id,
        description="A test task",
        date_due=due_date
    )
    assert task.name == "Test Task"
    assert task.element_id == sample_element.id
    assert task.home_id == sample_element.home_id
    assert task.description == "A test task"
    assert task.date_due == due_date
    assert isinstance(task.id, uuid.UUID)

def test_model_relationships(test_session, sample_home, sample_room, sample_element):
    """Test relationships between models."""
    # Test Home -> Room relationship
    rooms = test_session.query(Room).filter(Room.home_id == sample_home.id).all()
    assert len(rooms) > 0
    assert rooms[0].home_id == sample_home.id

    # Test Room -> Element relationship
    elements = test_session.query(Element).filter(Element.room_id == sample_room.id).all()
    assert len(elements) > 0
    assert elements[0].room_id == sample_room.id

    # Test Element -> Task relationship
    tasks = test_session.query(Task).filter(Task.element_id == sample_element.id).all()
    assert len(tasks) > 0
    assert tasks[0].element_id == sample_element.id 