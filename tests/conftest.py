import os
import sys
import pytest
from sqlmodel import SQLModel, create_engine
from sqlalchemy.pool import StaticPool

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine."""
    return create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

@pytest.fixture(scope="session", autouse=True)
def setup_database(test_engine):
    """Set up the test database."""
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine) 