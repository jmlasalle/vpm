import pytest
from typer.testing import CliRunner
from vpm.tasks import app
from vpm.home import app as home_app
from vpm.room import app as room_app
from vpm.elements import app as element_app
from datetime import datetime, timedelta

runner = CliRunner()

def test_task_help():
    """Test task help command."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout

def test_task_add():
    """Test adding a task."""
    # First add a home, room, and element
    home_app.invoke(app, ["add", "--name", "Test Home", "--address", "123 Test St", "--description", "Test Description"])
    room_app.invoke(app, ["add", "--name", "Test Room"])
    element_app.invoke(app, [
        "add",
        "--name", "Test Element",
        "--type", "MAINTENANCE",
        "--description", "Test Description"
    ])
    
    # Then add a task
    result = runner.invoke(app, [
        "add",
        "--name", "Test Task",
        "--type", "MAINTENANCE",
        "--description", "Test Description",
        "--due-date", (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    ])
    assert result.exit_code == 0
    assert "Test Task" in result.stdout

def test_task_get():
    """Test getting task information."""
    # First add a home, room, element, and task
    home_app.invoke(app, ["add", "--name", "Test Home", "--address", "123 Test St", "--description", "Test Description"])
    room_app.invoke(app, ["add", "--name", "Test Room"])
    element_app.invoke(app, [
        "add",
        "--name", "Test Element",
        "--type", "MAINTENANCE",
        "--description", "Test Description"
    ])
    runner.invoke(app, [
        "add",
        "--name", "Test Task",
        "--type", "MAINTENANCE",
        "--description", "Test Description",
        "--due-date", (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    ])
    
    # Then get it
    result = runner.invoke(app, ["get", "--name", "Test Task"])
    assert result.exit_code == 0
    assert "Test Task" in result.stdout
    assert "MAINTENANCE" in result.stdout

def test_task_update():
    """Test updating a task."""
    # First add a home, room, element, and task
    home_app.invoke(app, ["add", "--name", "Test Home", "--address", "123 Test St", "--description", "Test Description"])
    room_app.invoke(app, ["add", "--name", "Test Room"])
    element_app.invoke(app, [
        "add",
        "--name", "Test Element",
        "--type", "MAINTENANCE",
        "--description", "Test Description"
    ])
    runner.invoke(app, [
        "add",
        "--name", "Test Task",
        "--type", "MAINTENANCE",
        "--description", "Test Description",
        "--due-date", (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    ])
    
    # Then update it
    result = runner.invoke(app, [
        "update",
        "--name", "Test Task",
        "--new-name", "Updated Task",
        "--type", "REPAIR"
    ])
    assert result.exit_code == 0
    assert "Updated Task" in result.stdout
    assert "REPAIR" in result.stdout

def test_task_complete():
    """Test completing a task."""
    # First add a home, room, element, and task
    home_app.invoke(app, ["add", "--name", "Test Home", "--address", "123 Test St", "--description", "Test Description"])
    room_app.invoke(app, ["add", "--name", "Test Room"])
    element_app.invoke(app, [
        "add",
        "--name", "Test Element",
        "--type", "MAINTENANCE",
        "--description", "Test Description"
    ])
    runner.invoke(app, [
        "add",
        "--name", "Test Task",
        "--type", "MAINTENANCE",
        "--description", "Test Description",
        "--due-date", (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    ])
    
    # Then complete it
    result = runner.invoke(app, ["complete", "--name", "Test Task"])
    assert result.exit_code == 0
    assert "Task marked as complete" in result.stdout

def test_task_delete():
    """Test deleting a task."""
    # First add a home, room, element, and task
    home_app.invoke(app, ["add", "--name", "Test Home", "--address", "123 Test St", "--description", "Test Description"])
    room_app.invoke(app, ["add", "--name", "Test Room"])
    element_app.invoke(app, [
        "add",
        "--name", "Test Element",
        "--type", "MAINTENANCE",
        "--description", "Test Description"
    ])
    runner.invoke(app, [
        "add",
        "--name", "Test Task",
        "--type", "MAINTENANCE",
        "--description", "Test Description",
        "--due-date", (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    ])
    
    # Then delete it
    result = runner.invoke(app, ["delete", "--name", "Test Task"])
    assert result.exit_code == 0
    assert "Task deleted" in result.stdout 