#!/bin/zsh
source .venv/bin/activate

# Install build dependencies
pip install build wheel twine

# Remove old builds
rm -rf dist/*

# Build the package
python -m build

# Upload the package    
twine upload dist/*  --verbose