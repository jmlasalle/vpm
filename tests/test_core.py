import pytest
from datetime import datetime
from vpm.services.property import HomeService, RoomService
from vpm.services.elements import ElementService, TaskService
from vpm.services.database import DatabaseService
from vpm.services.demo import DemoService
from vpm.utils.helpers import next_date
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

@pytest.fixture
def database_service():
    return DatabaseService()

@pytest.fixture
def demo_service():
    return DemoService()

def test_next_date():
    """Test the next_date utility function."""
    dt = datetime(2024, 1, 1)
    
    # Test yearly
    next_year = next_date("YEARLY", 1, dt)
    assert next_year.year == 2025
    assert next_year.month == 1
    assert next_year.day == 1
    
    # Test monthly
    next_month = next_date("MONTHLY", 1, dt)
    assert next_month.year == 2024
    assert next_month.month == 2
    assert next_month.day == 1
    
    # Test weekly
    next_week = next_date("WEEKLY", 1, dt)
    assert next_week.year == 2024
    assert next_week.month == 1
    assert next_week.day == 8
    
    # Test daily
    next_day = next_date("DAILY", 1, dt)
    assert next_day.year == 2024
    assert next_day.month == 1
    assert next_day.day == 2
    
    # Test invalid frequency
    with pytest.raises(ValueError):
        next_date("INVALID", 1, dt) 