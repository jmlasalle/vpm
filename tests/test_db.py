import pytest
from typer.testing import CliRunner
from vpm.db import app
import os
from pathlib import Path

runner = CliRunner()

def test_db_help():
    """Test DB help command."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout

def test_db_create():
    """Test creating a database."""
    result = runner.invoke(app, ["create", "--overwrite", "true"])
    assert result.exit_code == 0
    assert "sqlite" in result.stdout.lower()

def test_db_info():
    """Test getting database info."""
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "sqlite" in result.stdout.lower()

def test_db_create_no_overwrite():
    """Test creating a database without overwrite."""
    # First create the database
    runner.invoke(app, ["create", "--overwrite", "true"])
    
    # Try to create again without overwrite
    result = runner.invoke(app, ["create"])
    assert result.exit_code == 0
    assert "FileExistsError" in result.stdout 