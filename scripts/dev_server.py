#!/usr/bin/env python3
"""
Development script for MCP Verilog Server
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Set up the development environment"""
    try:
        # Create virtual environment if it doesn't exist
        venv_path = Path(".venv")
        if not venv_path.exists():
            logger.info("Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        
        # Get the Python executable from the virtual environment
        if sys.platform == "win32":
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            python_path = venv_path / "bin" / "python"
        
        # Install dependencies
        logger.info("Installing dependencies...")
        subprocess.run([str(python_path), "-m", "pip", "install", "-e", ".[dev]"], check=True)
        
        # Create necessary directories
        Path("mcp_output").mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
        
        return python_path
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to set up environment: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error during setup: {str(e)}")
        sys.exit(1)

def run_server(python_path):
    """Run the MCP server"""
    try:
        logger.info("Starting MCP server...")
        server_script = Path("src") / "mcp_server.py"
        
        # Set environment variables
        env = os.environ.copy()
        env["PYTHONPATH"] = str(Path.cwd())
        env["LOG_LEVEL"] = "DEBUG"
        
        # Run the server
        subprocess.run(
            [str(python_path), str(server_script)],
            env=env,
            check=True
        )
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Server failed to start: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error while running server: {str(e)}")
        sys.exit(1)

def main():
    """Main entry point"""
    try:
        # Set up the environment
        python_path = setup_environment()
        
        # Run the server
        run_server(python_path)
        
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 