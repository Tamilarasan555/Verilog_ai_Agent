from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import json
from pathlib import Path
import logging
import traceback
from datetime import datetime
import sys
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_client_debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add debug logging decorator
def debug_log(func):
    async def wrapper(*args, **kwargs):
        start_time = datetime.now()
        logger.debug(f"Starting {func.__name__} with args: {args}, kwargs: {kwargs}")
        
        try:
            result = await func(*args, **kwargs)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.debug(f"Completed {func.__name__} in {duration:.2f} seconds")
            return result
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.error(f"Error in {func.__name__} after {duration:.2f} seconds: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    return wrapper

@debug_log
async def analyze_syntax(verilog_code: str) -> Dict[str, Any]:
    """Analyze Verilog code for syntax errors"""
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            try:
                await session.initialize()
                result = await session.call_tool(
                    "analyze_syntax",
                    arguments={"verilog_code": verilog_code}
                )
                return result
            except Exception as e:
                logger.error(f"Syntax analysis failed: {str(e)}")
                raise

@debug_log
async def analyze_simulation(verilog_code: str, testbench: str) -> Dict[str, Any]:
    """Analyze simulation behavior"""
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            try:
                await session.initialize()
                result = await session.call_tool(
                    "analyze_simulation",
                    arguments={
                        "verilog_code": verilog_code,
                        "testbench": testbench
                    }
                )
                return result
            except Exception as e:
                logger.error(f"Simulation analysis failed: {str(e)}")
                raise

@debug_log
async def analyze_synthesis(verilog_code: str) -> Dict[str, Any]:
    """Analyze synthesis issues"""
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            try:
                await session.initialize()
                result = await session.call_tool(
                    "analyze_synthesis",
                    arguments={"verilog_code": verilog_code}
                )
                return result
            except Exception as e:
                logger.error(f"Synthesis analysis failed: {str(e)}")
                raise

@debug_log
async def analyze_formal_verification(verilog_code: str) -> Dict[str, Any]:
    """Analyze formal verification issues"""
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            try:
                await session.initialize()
                result = await session.call_tool(
                    "analyze_formal_verification",
                    arguments={"verilog_code": verilog_code}
                )
                return result
            except Exception as e:
                logger.error(f"Formal verification analysis failed: {str(e)}")
                raise

@debug_log
async def debug_design(verilog_code: str, error_message: str, context: str = "") -> Dict[str, Any]:
    """Enhanced debugging function"""
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            try:
                await session.initialize()
                
                # Get debug prompt
                prompt = await session.get_prompt(
                    "debug_prompt",
                    arguments={
                        "verilog_code": verilog_code,
                        "error_message": error_message,
                        "context": context
                    }
                )
                
                # Perform comprehensive analysis
                syntax_result = await analyze_syntax(verilog_code)
                synthesis_result = await analyze_synthesis(verilog_code)
                formal_result = await analyze_formal_verification(verilog_code)
                
                return {
                    "debug_prompt": prompt,
                    "syntax_analysis": syntax_result,
                    "synthesis_analysis": synthesis_result,
                    "formal_verification": formal_result
                }
                
            except Exception as e:
                logger.error(f"Debugging failed: {str(e)}")
                raise

@debug_log
async def generate_verilog_design(description: str, module_name: Optional[str] = None) -> Dict[str, Any]:
    """Generate a complete Verilog design using the AI Agent"""
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_verilog_agent.py"],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            try:
                await session.initialize()
                result = await session.call_tool(
                    "generate_design",
                    arguments={
                        "description": description,
                        "module_name": module_name
                    }
                )
                return result
            except Exception as e:
                logger.error(f"Design generation failed: {str(e)}")
                raise

@debug_log
async def optimize_design(verilog_code: str) -> Dict[str, Any]:
    """Optimize a Verilog design"""
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_verilog_agent.py"],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            try:
                await session.initialize()
                result = await session.call_tool(
                    "optimize_design",
                    arguments={"verilog_code": verilog_code}
                )
                return result
            except Exception as e:
                logger.error(f"Design optimization failed: {str(e)}")
                raise

@debug_log
async def verify_design(verilog_code: str, testbench: str) -> Dict[str, Any]:
    """Verify a Verilog design"""
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_verilog_agent.py"],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            try:
                await session.initialize()
                result = await session.call_tool(
                    "verify_design",
                    arguments={
                        "verilog_code": verilog_code,
                        "testbench": testbench
                    }
                )
                return result
            except Exception as e:
                logger.error(f"Design verification failed: {str(e)}")
                raise

@debug_log
async def generate_documentation(verilog_code: str, testbench: str) -> Dict[str, Any]:
    """Generate documentation for a Verilog design"""
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_verilog_agent.py"],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            try:
                await session.initialize()
                result = await session.call_tool(
                    "generate_documentation",
                    arguments={
                        "verilog_code": verilog_code,
                        "testbench": testbench
                    }
                )
                return result
            except Exception as e:
                logger.error(f"Documentation generation failed: {str(e)}")
                raise

@debug_log
async def get_design(design_id: str) -> Dict[str, Any]:
    """Retrieve a previously generated design"""
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_verilog_agent.py"],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            try:
                await session.initialize()
                result = await session.call_tool(
                    "get_design",
                    arguments={"design_id": design_id}
                )
                return result
            except Exception as e:
                logger.error(f"Failed to retrieve design: {str(e)}")
                raise

async def main():
    """Main entry point for the MCP client"""
    try:
        # Example: Generate a RISC processor design
        description = """
        Design a 5-stage pipelined RISC processor core with the following specifications:
        - 32-bit instruction set
        - 32-bit data path
        - 32 general-purpose registers
        - 4KB instruction cache
        - 4KB data cache
        - Branch prediction
        - Forwarding unit
        - Hazard detection
        """
        
        # Generate the design
        design_result = await generate_verilog_design(description, "risc_processor")
        logger.info("Design generated successfully!")
        
        # Get the generated files
        design_id = design_result["files"]["original"]["verilog"].stem
        design_files = await get_design(design_id)
        logger.info(f"Retrieved design files: {list(design_files['files'].keys())}")
        
        # Optimize the design
        optimization_result = await optimize_design(design_files["files"]["risc_processor.v"])
        logger.info("Design optimized successfully!")
        
        # Verify the design
        verification_result = await verify_design(
            optimization_result["optimized_file"],
            design_files["files"]["risc_processor_tb.sv"]
        )
        logger.info("Design verified successfully!")
        
        # Generate documentation
        doc_result = await generate_documentation(
            optimization_result["optimized_file"],
            design_files["files"]["risc_processor_tb.sv"]
        )
        logger.info("Documentation generated successfully!")
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 