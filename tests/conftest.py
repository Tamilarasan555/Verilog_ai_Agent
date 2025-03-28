"""
Pytest configuration for MCP Verilog tests
"""

import pytest
import asyncio
import logging
from pathlib import Path
from typing import Generator

# Configure logging for tests
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for the test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_dir() -> Path:
    """Get the test directory path"""
    return Path(__file__).parent

@pytest.fixture(scope="session")
def output_dir(test_dir: Path) -> Path:
    """Create and return the test output directory"""
    output_dir = test_dir / "test_output"
    output_dir.mkdir(exist_ok=True)
    yield output_dir
    # Clean up test output after tests
    for item in output_dir.glob("*"):
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            for subitem in item.glob("*"):
                subitem.unlink()
            item.rmdir() 