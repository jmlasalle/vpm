import pytest
from typer.testing import CliRunner
from vpm.elements import app
from vpm.home import app as home_app
from vpm.room import app as room_app

runner = CliRunner()

def test_element_help():
    """Test element help command."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout

def test_element_add():
    """Test adding an element."""
    # First add a home and room
    home_app.invoke(app, ["add", "--name", "Test Home", "--address", "123 Test St", "--description", "Test Description"])
    room_app.invoke(app, ["add", "--name", "Test Room"])
    
    # Then add an element
    result = runner.invoke(app, [
        "add",
        "--name", "Test Element",
        "--type", "MAINTENANCE",
        "--description", "Test Description"
    ])
    assert result.exit_code == 0
    assert "Test Element" in result.stdout

def test_element_get():
    """Test getting element information."""
    # First add a home, room, and element
    home_app.invoke(app, ["add", "--name", "Test Home", "--address", "123 Test St", "--description", "Test Description"])
    room_app.invoke(app, ["add", "--name", "Test Room"])
    runner.invoke(app, [
        "add",
        "--name", "Test Element",
        "--type", "MAINTENANCE",
        "--description", "Test Description"
    ])
    
    # Then get it
    result = runner.invoke(app, ["get", "--name", "Test Element"])
    assert result.exit_code == 0
    assert "Test Element" in result.stdout
    assert "MAINTENANCE" in result.stdout

def test_element_update():
    """Test updating an element."""
    # First add a home, room, and element
    home_app.invoke(app, ["add", "--name", "Test Home", "--address", "123 Test St", "--description", "Test Description"])
    room_app.invoke(app, ["add", "--name", "Test Room"])
    runner.invoke(app, [
        "add",
        "--name", "Test Element",
        "--type", "MAINTENANCE",
        "--description", "Test Description"
    ])
    
    # Then update it
    result = runner.invoke(app, [
        "update",
        "--name", "Test Element",
        "--new-name", "Updated Element",
        "--type", "REPAIR"
    ])
    assert result.exit_code == 0
    assert "Updated Element" in result.stdout
    assert "REPAIR" in result.stdout

def test_element_delete():
    """Test deleting an element."""
    # First add a home, room, and element
    home_app.invoke(app, ["add", "--name", "Test Home", "--address", "123 Test St", "--description", "Test Description"])
    room_app.invoke(app, ["add", "--name", "Test Room"])
    runner.invoke(app, [
        "add",
        "--name", "Test Element",
        "--type", "MAINTENANCE",
        "--description", "Test Description"
    ])
    
    # Then delete it
    result = runner.invoke(app, ["delete", "--name", "Test Element"])
    assert result.exit_code == 0
    assert "Element deleted" in result.stdout 