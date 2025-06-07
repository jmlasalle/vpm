import pytest
from uuid import uuid4
from datetime import datetime, timezone
from vpm.services.property import HomeService, RoomService
from vpm.services.elements import ElementService, TaskService
from vpm.models.property import Home, Room
from vpm.models.elements import Element, Task
from vpm.database import init_db, create_home_trigger

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    init_db()
    create_home_trigger()
    yield
    # Cleanup after test

@pytest.fixture
def home_service():
    return HomeService()

@pytest.fixture
def room_service():
    return RoomService()

@pytest.fixture
def element_service():
    return ElementService()

@pytest.fixture
def task_service():
    return TaskService()

def test_create_home(home_service):
    """Test creating a home."""
    home = Home(
        name="Test Home",
        address="123 Test St"
    )
    created = home_service.create(home)
    assert created.id is not None
    assert created.name == "Test Home"
    assert created.address == "123 Test St"

def test_create_room(room_service, home_service):
    """Test creating a room."""
    # First create a home
    home = home_service.create(Home(
        name="Test Home",
        address="123 Test St"
    ))
    
    # Then create a room
    room = Room(
        name="Test Room",
        level=1,
        home_id=home.id
    )
    created = room_service.create(room)
    assert created.id is not None
    assert created.name == "Test Room"
    assert created.level == 1
    assert created.home_id == home.id

def test_create_element(element_service, room_service, home_service):
    """Test creating an element."""
    # First create a home and room
    home = home_service.create(Home(
        name="Test Home",
        address="123 Test St"
    ))
    room = room_service.create(Room(
        name="Test Room",
        level=1,
        home_id=home.id
    ))
    
    # Then create an element
    element = Element(
        name="Test Element",
        room_id=room.id
    )
    created = element_service.create(element)
    assert created.id is not None
    assert created.name == "Test Element"
    assert created.room_id == room.id

def test_create_task(task_service, element_service, room_service, home_service):
    """Test creating a task."""
    # First create a home, room, and element
    home = home_service.create(Home(
        name="Test Home",
        address="123 Test St"
    ))
    room = room_service.create(Room(
        name="Test Room",
        level=1,
        home_id=home.id
    ))
    element = element_service.create(Element(
        name="Test Element",
        room_id=room.id
    ))
    
    # Then create a task
    task = Task(
        name="Test Task",
        interval=1,
        interval_unit="month",
        element_id=element.id
    )
    created = task_service.create(task)
    assert created.id is not None
    assert created.name == "Test Task"
    assert created.interval == 1
    assert created.interval_unit == "month"
    assert created.element_id == element.id 