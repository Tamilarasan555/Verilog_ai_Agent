import asyncio
import logging
from pathlib import Path
from mcp_client import (
    generate_verilog_design,
    debug_design,
    optimize_design,
    analyze_syntax,
    analyze_simulation,
    analyze_synthesis,
    analyze_formal_verification
)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def test_design_analysis():
    """Test design analysis tool"""
    description = """
    Create a 4-bit ALU with the following specifications:
    - Clock input (clk)
    - Active high reset (rst_n)
    - 4-bit inputs (a, b)
    - 2-bit operation select (op)
    - 4-bit output (result)
    - Zero flag output (zero)
    - Operations: ADD, SUB, AND, OR
    """
    
    try:
        result = await generate_verilog_design(description)
        logger.info("Design analysis test completed successfully")
        return result
    except Exception as e:
        logger.error(f"Design analysis test failed: {str(e)}")
        raise

async def test_syntax_analysis():
    """Test syntax analysis tool"""
    # Read the generated ALU code
    alu_code = Path("test_output/alu_4bit.v").read_text()
    
    try:
        result = await analyze_syntax(alu_code)
        logger.info("Syntax analysis test completed successfully")
        return result
    except Exception as e:
        logger.error(f"Syntax analysis test failed: {str(e)}")
        raise

async def test_simulation_analysis():
    """Test simulation analysis tool"""
    # Read the generated ALU code and testbench
    alu_code = Path("test_output/alu_4bit.v").read_text()
    testbench = Path("test_output/alu_4bit_tb.sv").read_text()
    
    try:
        result = await analyze_simulation(alu_code, testbench)
        logger.info("Simulation analysis test completed successfully")
        return result
    except Exception as e:
        logger.error(f"Simulation analysis test failed: {str(e)}")
        raise

async def test_synthesis_analysis():
    """Test synthesis analysis tool"""
    # Read the generated ALU code
    alu_code = Path("test_output/alu_4bit.v").read_text()
    
    try:
        result = await analyze_synthesis(alu_code)
        logger.info("Synthesis analysis test completed successfully")
        return result
    except Exception as e:
        logger.error(f"Synthesis analysis test failed: {str(e)}")
        raise

async def test_formal_verification():
    """Test formal verification analysis tool"""
    # Read the generated ALU code
    alu_code = Path("test_output/alu_4bit.v").read_text()
    
    try:
        result = await analyze_formal_verification(alu_code)
        logger.info("Formal verification test completed successfully")
        return result
    except Exception as e:
        logger.error(f"Formal verification test failed: {str(e)}")
        raise

async def test_debugging():
    """Test debugging tool"""
    # Read the generated ALU code
    alu_code = Path("test_output/alu_4bit.v").read_text()
    error_msg = "Setup time violation in ALU module"
    context = "The error occurs during synthesis with a 100MHz clock constraint"
    
    try:
        result = await debug_design(alu_code, error_msg, context)
        logger.info("Debugging test completed successfully")
        return result
    except Exception as e:
        logger.error(f"Debugging test failed: {str(e)}")
        raise

async def test_optimization():
    """Test optimization tool"""
    # Read the generated ALU code
    alu_code = Path("test_output/alu_4bit.v").read_text()
    
    try:
        result = await optimize_design(alu_code, "power")
        logger.info("Optimization test completed successfully")
        return result
    except Exception as e:
        logger.error(f"Optimization test failed: {str(e)}")
        raise

async def run_all_tests():
    """Run all MCP tool tests"""
    logger.info("Starting MCP tool tests...")
    
    try:
        # Test design analysis
        logger.info("Testing design analysis...")
        design_result = await test_design_analysis()
        
        # Test syntax analysis
        logger.info("Testing syntax analysis...")
        syntax_result = await test_syntax_analysis()
        
        # Test simulation analysis
        logger.info("Testing simulation analysis...")
        simulation_result = await test_simulation_analysis()
        
        # Test synthesis analysis
        logger.info("Testing synthesis analysis...")
        synthesis_result = await test_synthesis_analysis()
        
        # Test formal verification
        logger.info("Testing formal verification...")
        formal_result = await test_formal_verification()
        
        # Test debugging
        logger.info("Testing debugging...")
        debug_result = await test_debugging()
        
        # Test optimization
        logger.info("Testing optimization...")
        opt_result = await test_optimization()
        
        logger.info("All MCP tool tests completed successfully!")
        
        return {
            "design": design_result,
            "syntax": syntax_result,
            "simulation": simulation_result,
            "synthesis": synthesis_result,
            "formal": formal_result,
            "debug": debug_result,
            "optimization": opt_result
        }
        
    except Exception as e:
        logger.error(f"Test suite failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(run_all_tests()) 