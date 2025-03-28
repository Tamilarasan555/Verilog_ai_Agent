#!/usr/bin/env python3
"""
Project setup script
"""

import os
import shutil
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_directories():
    """Create necessary project directories"""
    directories = [
        "src/mcp_verilog",
        "src/mcp_verilog/agents",
        "src/mcp_verilog/tools",
        "src/mcp_verilog/utils",
        "tests/unit",
        "tests/integration",
        "tests/fixtures",
        "docs",
        "logs",
        "mcp_output",
        "test_output"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")

def move_files():
    """Move files to their correct locations"""
    # Move Python files to src/mcp_verilog
    src_files = {
        "verilog_ai_agent.py": "src/mcp_verilog/agents/",
        "verilog_generator.py": "src/mcp_verilog/tools/",
        "design_optimizer.py": "src/mcp_verilog/tools/",
        "design_verifier.py": "src/mcp_verilog/tools/",
        "doc_generator.py": "src/mcp_verilog/tools/",
        "code_quality_analyzer.py": "src/mcp_verilog/tools/",
        "mcp_server.py": "src/mcp_verilog/",
        "mcp_client.py": "src/mcp_verilog/",
    }
    
    for file, dest in src_files.items():
        if Path(file).exists():
            shutil.move(file, Path(dest) / file)
            logger.info(f"Moved {file} to {dest}")
    
    # Move test files to tests
    test_files = {
        "test_mcp_server.py": "tests/integration/",
        "test_examples.py": "tests/unit/",
        "test_mcp_verilog.py": "tests/integration/",
        "test_mcp_cli.py": "tests/integration/",
        "test_mcp_tools.py": "tests/unit/",
        "test_risc_processor.py": "tests/unit/",
    }
    
    for file, dest in test_files.items():
        if Path(file).exists():
            shutil.move(file, Path(dest) / file)
            logger.info(f"Moved {file} to {dest}")
    
    # Move log files to logs
    for log_file in Path(".").glob("*.log"):
        shutil.move(str(log_file), Path("logs") / log_file.name)
        logger.info(f"Moved {log_file.name} to logs/")

def create_init_files():
    """Create __init__.py files"""
    init_locations = [
        "src/mcp_verilog",
        "src/mcp_verilog/agents",
        "src/mcp_verilog/tools",
        "src/mcp_verilog/utils",
        "tests/unit",
        "tests/integration",
        "tests/fixtures"
    ]
    
    for location in init_locations:
        init_file = Path(location) / "__init__.py"
        init_file.touch()
        logger.info(f"Created {init_file}")

def create_env_example():
    """Create .env.example file"""
    env_example = """# API Keys
OPENAI_API_KEY=your_openai_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO

# Verilog Configuration
VERILOG_TOOL_PATH=/path/to/verilog/tools
"""
    
    Path(".env.example").write_text(env_example)
    logger.info("Created .env.example")

def main():
    """Main entry point"""
    try:
        logger.info("Setting up project structure...")
        create_directories()
        move_files()
        create_init_files()
        create_env_example()
        logger.info("Project setup completed successfully!")
        
    except Exception as e:
        logger.error(f"Project setup failed: {str(e)}")
        raise

if __name__ == "__main__":
    main() 