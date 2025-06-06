import pytest
from typer.testing import CliRunner
from vpm.cli import app

runner = CliRunner()

def test_cli_help():
    """Test CLI help command."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout

def test_cli_version():
    """Test version command."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "Version" in result.stdout

def test_cli_onboard():
    """Test onboarding process."""
    # Use input to simulate user responses
    result = runner.invoke(app, ["onboard"], input="Test Home\n123 Test St\nTest Room\ny\nTest Element\ntest_equipment\n2024-01-01\nn\nn\n")
    assert result.exit_code == 0
    assert "Welcome to vpm!" in result.stdout

def test_cli_dashboard():
    """Test dashboard command."""
    # First create a home through onboarding
    runner.invoke(app, ["onboard"], input="Test Home\n123 Test St\nTest Room\ny\nTest Element\ntest_equipment\n2024-01-01\nn\nn\n")
    
    # Get the home ID from the output (you might need to adjust this based on your actual output format)
    result = runner.invoke(app, ["home", "get"])
    assert result.exit_code == 0
    home_id = result.stdout.strip()  # You might need to parse this to get the actual ID
    
    # Test dashboard
    result = runner.invoke(app, ["dashboard", home_id])
    assert result.exit_code == 0
    assert "Test Home" in result.stdout
    assert "Test Room" in result.stdout

def test_cli_subcommands():
    """Test that all subcommands are available."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "home" in result.stdout
    assert "room" in result.stdout
    assert "element" in result.stdout
    assert "task" in result.stdout
    assert "part" in result.stdout
    assert "db" in result.stdout

def test_cli_add_home():
    """Test adding a home via CLI."""
    result = runner.invoke(app, ["add", "home", "--name", "Test Home", "--address", "123 Test St"])
    assert result.exit_code == 0
    assert "Home added successfully" in result.stdout

def test_cli_add_room():
    """Test adding a room via CLI."""
    # First add a home
    runner.invoke(app, ["add", "home", "--name", "Test Home", "--address", "123 Test St"])
    
    # Then add a room
    result = runner.invoke(app, ["add", "room", "--name", "Test Room", "--home", "Test Home"])
    assert result.exit_code == 0
    assert "Room added successfully" in result.stdout

def test_cli_add_element():
    """Test adding an element via CLI."""
    # First add a home and room
    runner.invoke(app, ["add", "home", "--name", "Test Home", "--address", "123 Test St"])
    runner.invoke(app, ["add", "room", "--name", "Test Room", "--home", "Test Home"])
    
    # Then add an element
    result = runner.invoke(app, [
        "add", "element",
        "--name", "Test Element",
        "--type", "test_equipment",
        "--room", "Test Room"
    ])
    assert result.exit_code == 0
    assert "Element added successfully" in result.stdout

def test_cli_list_homes():
    """Test listing homes via CLI."""
    # First add a home
    runner.invoke(app, ["add", "home", "--name", "Test Home", "--address", "123 Test St"])
    
    # Then list homes
    result = runner.invoke(app, ["list", "homes"])
    assert result.exit_code == 0
    assert "Test Home" in result.stdout

def test_cli_list_rooms():
    """Test listing rooms via CLI."""
    # First add a home and room
    runner.invoke(app, ["add", "home", "--name", "Test Home", "--address", "123 Test St"])
    runner.invoke(app, ["add", "room", "--name", "Test Room", "--home", "Test Home"])
    
    # Then list rooms
    result = runner.invoke(app, ["list", "rooms", "--home", "Test Home"])
    assert result.exit_code == 0
    assert "Test Room" in result.stdout

def test_cli_list_elements():
    """Test listing elements via CLI."""
    # First add a home, room, and element
    runner.invoke(app, ["add", "home", "--name", "Test Home", "--address", "123 Test St"])
    runner.invoke(app, ["add", "room", "--name", "Test Room", "--home", "Test Home"])
    runner.invoke(app, [
        "add", "element",
        "--name", "Test Element",
        "--type", "test_equipment",
        "--room", "Test Room"
    ])
    
    # Then list elements
    result = runner.invoke(app, ["list", "elements", "--room", "Test Room"])
    assert result.exit_code == 0
    assert "Test Element" in result.stdout

def test_cli_update_home():
    """Test updating a home via CLI."""
    # First add a home
    runner.invoke(app, ["add", "home", "--name", "Test Home", "--address", "123 Test St"])
    
    # Then update it
    result = runner.invoke(app, [
        "update", "home",
        "--name", "Test Home",
        "--new-name", "Updated Home"
    ])
    assert result.exit_code == 0
    assert "Home updated successfully" in result.stdout

def test_cli_delete_home():
    """Test deleting a home via CLI."""
    # First add a home
    runner.invoke(app, ["add", "home", "--name", "Test Home", "--address", "123 Test St"])
    
    # Then delete it
    result = runner.invoke(app, ["delete", "home", "--name", "Test Home"])
    assert result.exit_code == 0
    assert "Home deleted successfully" in result.stdout 