import asyncio
import json
import logging
from pathlib import Path
import os
from dotenv import load_dotenv
import subprocess

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_cli_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_mcp_command(command):
    """Run an MCP CLI command and return the output"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e.stderr}")
        raise

def test_mcp_tools():
    """Test MCP CLI tools"""
    try:
        # Test design analysis
        logger.info("Testing design analysis...")
        design_desc = """
        Design a 4-bit counter with the following specifications:
        - Clock input (clk)
        - Active high reset (rst_n)
        - 4-bit output (count)
        - Enable input (en)
        - Count up when enabled
        - Reset to 0 when rst_n is low
        """
        
        # Save design description to a file
        with open("design_desc.txt", "w") as f:
            f.write(design_desc)
        
        # Run design analysis
        design_spec = run_mcp_command("mcp analyze_design design_desc.txt")
        logger.info("Design analysis result:")
        logger.info(design_spec)
        
        # Save design spec
        with open("design_spec.json", "w") as f:
            f.write(design_spec)
        
        # Test code generation
        logger.info("Testing code generation...")
        verilog_code = run_mcp_command("mcp generate_verilog design_spec.json")
        logger.info("Generated Verilog code:")
        logger.info(verilog_code)
        
        # Save Verilog code
        with open("counter_4bit.v", "w") as f:
            f.write(verilog_code)
        
        # Test testbench generation
        logger.info("Testing testbench generation...")
        testbench = run_mcp_command("mcp generate_testbench counter_4bit design_spec.json")
        logger.info("Generated testbench:")
        logger.info(testbench)
        
        # Save testbench
        with open("counter_4bit_tb.sv", "w") as f:
            f.write(testbench)
        
        # Test optimization
        logger.info("Testing optimization...")
        optimized_code = run_mcp_command("mcp optimize_design counter_4bit.v --target area")
        logger.info("Optimized code:")
        logger.info(optimized_code)
        
        # Save optimized code
        with open("counter_4bit_optimized.v", "w") as f:
            f.write(optimized_code)
        
        # Test verification
        logger.info("Testing verification...")
        verification_result = run_mcp_command("mcp verify_design counter_4bit.v counter_4bit_tb.sv")
        logger.info("Verification result:")
        logger.info(verification_result)
        
        # Save verification result
        with open("verification_result.json", "w") as f:
            f.write(verification_result)
        
        # Create output directory and move files
        output_dir = Path("test_output")
        output_dir.mkdir(exist_ok=True)
        
        # Move all generated files to output directory
        files_to_move = [
            "design_desc.txt",
            "design_spec.json",
            "counter_4bit.v",
            "counter_4bit_tb.sv",
            "counter_4bit_optimized.v",
            "verification_result.json"
        ]
        
        for file in files_to_move:
            if os.path.exists(file):
                os.rename(file, output_dir / file)
        
        logger.info("All tests completed successfully!")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_mcp_tools() 