import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool
import uuid
from datetime import datetime
from vpm.database import engine
from vpm.models import Home, Room, Element, Task, TaskType

@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine."""
    return create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create a fresh database for each test."""
    SQLModel.metadata.create_all(test_engine)
    yield test_engine
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture(scope="function")
def test_session(test_db):
    """Create a new database session for each test."""
    with Session(test_db) as session:
        yield session

@pytest.fixture
def sample_home(test_session):
    """Create a sample home for testing."""
    home = Home(
        id=uuid.uuid4(),
        name="Test Home",
        address="123 Test St",
        description="A test home"
    )
    test_session.add(home)
    test_session.commit()
    test_session.refresh(home)
    return home

@pytest.fixture
def sample_room(test_session, sample_home):
    """Create a sample room for testing."""
    room = Room(
        id=uuid.uuid4(),
        name="Test Room",
        home_id=sample_home.id,
        level=1
    )
    test_session.add(room)
    test_session.commit()
    test_session.refresh(room)
    return room

@pytest.fixture
def sample_element(test_session, sample_room):
    """Create a sample element for testing."""
    element = Element(
        id=uuid.uuid4(),
        name="Test Element",
        equip_type="test_equipment",
        room_id=sample_room.id,
        home_id=sample_room.home_id,
        install_date=datetime.now()
    )
    test_session.add(element)
    test_session.commit()
    test_session.refresh(element)
    return element

@pytest.fixture
def sample_task_type(test_session):
    """Create a sample task type for testing."""
    task_type = TaskType(
        id=uuid.uuid4(),
        name="Test Task Type",
        equip_type="test_equipment",
        frequency="monthly",
        interval=1,
        description="A test task type"
    )
    test_session.add(task_type)
    test_session.commit()
    test_session.refresh(task_type)
    return task_type 