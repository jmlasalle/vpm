import pytest
from typer.testing import CliRunner
from vpm.room import app
from vpm.home import app as home_app

runner = CliRunner()

def test_room_help():
    """Test room help command."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout

def test_room_add():
    """Test adding a room."""
    # First add a home
    home_app.invoke(app, ["add", "--name", "Test Home", "--address", "123 Test St", "--description", "Test Description"])
    
    # Then add a room
    result = runner.invoke(app, ["add", "--name", "Test Room"])
    assert result.exit_code == 0
    assert "Test Room" in result.stdout

def test_room_get():
    """Test getting room information."""
    # First add a home and room
    home_app.invoke(app, ["add", "--name", "Test Home", "--address", "123 Test St", "--description", "Test Description"])
    runner.invoke(app, ["add", "--name", "Test Room"])
    
    # Then get it
    result = runner.invoke(app, ["get", "--name", "Test Room"])
    assert result.exit_code == 0
    assert "Test Room" in result.stdout

def test_room_update():
    """Test updating a room."""
    # First add a home and room
    home_app.invoke(app, ["add", "--name", "Test Home", "--address", "123 Test St", "--description", "Test Description"])
    runner.invoke(app, ["add", "--name", "Test Room"])
    
    # Then update it
    result = runner.invoke(app, ["update", "--name", "Test Room", "--new-name", "Updated Room"])
    assert result.exit_code == 0
    assert "Updated Room" in result.stdout

def test_room_delete():
    """Test deleting a room."""
    # First add a home and room
    home_app.invoke(app, ["add", "--name", "Test Home", "--address", "123 Test St", "--description", "Test Description"])
    runner.invoke(app, ["add", "--name", "Test Room"])
    
    # Then delete it
    result = runner.invoke(app, ["delete", "--name", "Test Room"])
    assert result.exit_code == 0
    assert "Room deleted" in result.stdout 