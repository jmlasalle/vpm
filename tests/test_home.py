import pytest
from typer.testing import CliRunner
from vpm.home import app

runner = CliRunner()

def test_home_help():
    """Test home help command."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout

def test_home_add():
    """Test adding a home."""
    result = runner.invoke(app, ["add", "--name", "Test Home", "--address", "123 Test St", "--description", "Test Description"])
    assert result.exit_code == 0
    assert "Test Home" in result.stdout

def test_home_get():
    """Test getting home information."""
    # First add a home
    runner.invoke(app, ["add", "--name", "Test Home", "--address", "123 Test St", "--description", "Test Description"])
    
    # Then get it
    result = runner.invoke(app, ["get"])
    assert result.exit_code == 0
    assert "Test Home" in result.stdout
    assert "123 Test St" in result.stdout

def test_home_update():
    """Test updating a home."""
    # First add a home
    runner.invoke(app, ["add", "--name", "Test Home", "--address", "123 Test St", "--description", "Test Description"])
    
    # Then update it
    result = runner.invoke(app, ["update", "--name", "Updated Home"])
    assert result.exit_code == 0
    assert "Updated Home" in result.stdout

def test_home_delete():
    """Test deleting a home."""
    # First add a home
    runner.invoke(app, ["add", "--name", "Test Home", "--address", "123 Test St", "--description", "Test Description"])
    
    # Then delete it
    result = runner.invoke(app, ["delete"])
    assert result.exit_code == 0
    assert "Home deleted" in result.stdout 