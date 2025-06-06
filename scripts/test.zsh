#!/bin/zsh

source .venv/bin/activate

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    echo "${2}${1}${NC}"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if we're in the project root
if [ ! -f "pyproject.toml" ]; then
    print_message "Error: Must run from project root directory" "$RED"
    exit 1
fi

# Check if pytest is installed
if ! command_exists pytest; then
    print_message "Error: pytest is not installed. Please install it with 'pip install pytest'" "$RED"
    exit 1
fi

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    print_message "Warning: Not running in a virtual environment" "$YELLOW"
    read -q "?Continue anyway? (y/n) " || exit 1
    echo
fi

# Parse command line arguments
VERBOSE=false
COVERAGE=false
TEST_PATH="tests"

while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -p|--path)
            TEST_PATH="$2"
            shift 2
            ;;
        *)
            print_message "Unknown option: $1" "$RED"
            exit 1
            ;;
    esac
done

# Build pytest command
PYTEST_CMD="pytest"

if [ "$VERBOSE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -v"
fi

if [ "$COVERAGE" = true ]; then
    if ! command_exists coverage; then
        print_message "Error: coverage is not installed. Please install it with 'pip install coverage'" "$RED"
        exit 1
    fi
    PYTEST_CMD="coverage run -m pytest"
fi

# Run the tests
print_message "Running tests in $TEST_PATH..." "$GREEN"
eval "$PYTEST_CMD $TEST_PATH"

# If coverage was requested, show the report
if [ "$COVERAGE" = true ]; then
    print_message "\nGenerating coverage report..." "$GREEN"
    coverage report
    coverage html
    print_message "Coverage report generated in htmlcov/index.html" "$GREEN"
fi

# Check the exit status
if [ $? -eq 0 ]; then
    print_message "\nAll tests passed! 🎉" "$GREEN"
else
    print_message "\nSome tests failed! 😢" "$RED"
    exit 1
fi 