import asyncio
import httpx
import json
import logging
import os
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_risc_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create output directory if it doesn't exist
Path("test_output").mkdir(exist_ok=True)

async def test_risc_processor():
    """Test the RISC processor design process"""
    logger.info("Testing RISC processor design...")
    
    # Design specification
    design_spec = {
        "description": """
        32-bit RISC processor core with the following features:
        - 5-stage pipeline (IF, ID, EX, MEM, WB)
        - 32 general-purpose registers
        - Basic instruction set (arithmetic, logic, load/store, branch)
        - Forwarding unit for data hazard handling
        - Branch prediction with 2-bit saturating counter
        - Separate instruction and data caches
        - Memory management unit with TLB
        - Interrupt handling capability
        """
    }
    
    try:
        # Step 1: Analyze design
        logger.info("Step 1: Analyzing design requirements...")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:9000/analyze",
                json=design_spec
            )
            response.raise_for_status()
            analysis_result = response.json()
            
            # Save analysis results
            with open("test_output/risc_analysis.json", "w") as f:
                json.dump(analysis_result, f, indent=2)
            logger.info("Design analysis completed and saved")
            
        # Step 2: Generate Verilog code
        logger.info("Step 2: Generating Verilog code...")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:9000/generate",
                json={"design_spec": analysis_result}
            )
            response.raise_for_status()
            verilog_result = response.json()
            
            # Save Verilog code
            with open("test_output/risc_core.v", "w") as f:
                f.write(verilog_result["verilog_code"])
            logger.info("Verilog code generated and saved")
            
        # Step 3: Generate testbench
        logger.info("Step 3: Generating testbench...")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:9000/testbench",
                json={
                    "module_name": analysis_result["module_name"],
                    "design_spec": analysis_result
                }
            )
            response.raise_for_status()
            testbench_result = response.json()
            
            # Save testbench
            with open("test_output/risc_core_tb.sv", "w") as f:
                f.write(testbench_result["testbench_code"])
            logger.info("Testbench generated and saved")
            
        # Step 4: Optimize design
        logger.info("Step 4: Optimizing design...")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:9000/optimize",
                json={
                    "verilog_code": verilog_result["verilog_code"],
                    "target": "performance"
                }
            )
            response.raise_for_status()
            optimize_result = response.json()
            
            # Save optimized code
            with open("test_output/risc_core_opt.v", "w") as f:
                f.write(optimize_result["optimized_code"])
            logger.info("Design optimization completed and saved")
            
        # Step 5: Verify design
        logger.info("Step 5: Verifying design...")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:9000/verify",
                json={
                    "verilog_code": optimize_result["optimized_code"],
                    "testbench": testbench_result["testbench_code"]
                }
            )
            response.raise_for_status()
            verify_result = response.json()
            
            # Save verification results
            with open("test_output/risc_verification.json", "w") as f:
                json.dump(verify_result, f, indent=2)
            logger.info("Design verification completed and saved")
            
        logger.info("RISC processor design process completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error during RISC processor design: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_risc_processor()) 