#!/usr/bin/env python3
"""
Test script for MCP Verilog integration
"""

import asyncio
import logging
from pathlib import Path
from mcp_client import (
    generate_verilog_design,
    optimize_design,
    verify_design,
    generate_documentation,
    get_design
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_mcp_verilog():
    """Test the MCP Verilog integration"""
    try:
        # Test design description
        description = """
        Design a simple 4-bit counter with the following specifications:
        - Clock input (clk)
        - Active high reset (rst_n)
        - Enable input (en)
        - 4-bit output (count)
        - Counts from 0 to 15
        - Rolls over to 0 after 15
        """
        
        # Generate the design
        logger.info("Generating design...")
        design_result = await generate_verilog_design(description, "counter")
        logger.info("Design generated successfully!")
        
        # Get the generated files
        design_id = design_result["files"]["original"]["verilog"].stem
        design_files = await get_design(design_id)
        logger.info(f"Retrieved design files: {list(design_files['files'].keys())}")
        
        # Optimize the design
        logger.info("Optimizing design...")
        optimization_result = await optimize_design(design_files["files"]["counter.v"])
        logger.info("Design optimized successfully!")
        
        # Verify the design
        logger.info("Verifying design...")
        verification_result = await verify_design(
            optimization_result["optimized_file"],
            design_files["files"]["counter_tb.sv"]
        )
        logger.info("Design verified successfully!")
        
        # Generate documentation
        logger.info("Generating documentation...")
        doc_result = await generate_documentation(
            optimization_result["optimized_file"],
            design_files["files"]["counter_tb.sv"]
        )
        logger.info("Documentation generated successfully!")
        
        # Print results
        logger.info("\nTest Results:")
        logger.info(f"Design ID: {design_id}")
        logger.info(f"Generated Files: {list(design_files['files'].keys())}")
        logger.info(f"Optimization Report: {optimization_result['report']}")
        logger.info(f"Verification Report: {verification_result['report']}")
        logger.info(f"Documentation Files: {list(doc_result.keys())}")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_mcp_verilog()) 