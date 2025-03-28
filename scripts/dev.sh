#!/bin/bash

# Exit on error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Setting up MCP Verilog development environment...${NC}"

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ $(echo "$python_version < 3.10" | bc) -eq 1 ]]; then
    echo -e "${RED}Error: Python 3.10 or later is required${NC}"
    exit 1
fi

# Create and activate virtual environment
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv .venv
fi

# Activate virtual environment
if [ "$OSTYPE" = "msys" ] || [ "$OSTYPE" = "win32" ]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -e ".[dev]"

# Run project setup script
echo -e "${YELLOW}Setting up project structure...${NC}"
python scripts/setup_project.py

# Run code formatting
echo -e "${YELLOW}Formatting code...${NC}"
black src tests
isort src tests

# Run type checking
echo -e "${YELLOW}Running type checks...${NC}"
mypy src

# Run linting
echo -e "${YELLOW}Running linter...${NC}"
ruff check src tests

# Run tests
echo -e "${YELLOW}Running tests...${NC}"
pytest

echo -e "${GREEN}Development environment setup completed!${NC}"
echo -e "${YELLOW}To start the server, run:${NC}"
echo -e "  python scripts/dev_server.py" 