#!/usr/bin/env python3
"""
MCP Server with Verilog AI Agent Integration
Provides a unified interface for Verilog design generation and analysis.
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mcp import Server, StdioServerParameters
from mcp.server.stdio import stdio_server
from verilog_ai_agent import VerilogAIAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="MCP Verilog Server", version="1.0.0")

# Initialize Verilog AI Agent
verilog_agent = VerilogAIAgent(output_dir="mcp_output")

# Initialize MCP server
server = Server()

class DesignRequest(BaseModel):
    """Request model for design generation"""
    description: str
    module_name: Optional[str] = None

class DesignResponse(BaseModel):
    """Response model for design generation"""
    files: Dict[str, Any]
    reports: Dict[str, Any]

# Register MCP tools
@server.tool("generate_design")
async def generate_design(description: str, module_name: Optional[str] = None) -> Dict[str, Any]:
    """Generate a complete Verilog design using the AI Agent"""
    try:
        results = await verilog_agent.process_design(
            description=description,
            module_name=module_name
        )
        return results
    except Exception as e:
        logger.error(f"Design generation failed: {str(e)}")
        raise

@server.tool("get_design")
async def get_design(design_id: str) -> Dict[str, Any]:
    """Retrieve a previously generated design"""
    try:
        design_dir = Path("mcp_output") / design_id
        if not design_dir.exists():
            raise ValueError("Design not found")
        
        # Read all relevant files
        files = {}
        for file_path in design_dir.glob("*"):
            if file_path.is_file():
                files[file_path.name] = file_path.read_text()
        
        return {
            "design_id": design_id,
            "files": files
        }
    except Exception as e:
        logger.error(f"Failed to retrieve design: {str(e)}")
        raise

@server.tool("optimize_design")
async def optimize_design(verilog_code: str) -> Dict[str, Any]:
    """Optimize an existing Verilog design"""
    try:
        # Save the code temporarily
        temp_file = Path("mcp_output") / "temp.v"
        temp_file.write_text(verilog_code)
        
        # Optimize the design
        optimization_results = verilog_agent.optimize_design(temp_file)
        
        # Clean up
        temp_file.unlink()
        
        return optimization_results
    except Exception as e:
        logger.error(f"Design optimization failed: {str(e)}")
        raise

@server.tool("verify_design")
async def verify_design(verilog_code: str, testbench: str) -> Dict[str, Any]:
    """Verify a Verilog design"""
    try:
        # Save the files temporarily
        temp_verilog = Path("mcp_output") / "temp.v"
        temp_tb = Path("mcp_output") / "temp_tb.sv"
        
        temp_verilog.write_text(verilog_code)
        temp_tb.write_text(testbench)
        
        # Verify the design
        verification_results = verilog_agent.verify_design(temp_verilog, temp_tb)
        
        # Clean up
        temp_verilog.unlink()
        temp_tb.unlink()
        
        return verification_results
    except Exception as e:
        logger.error(f"Design verification failed: {str(e)}")
        raise

@server.tool("generate_documentation")
async def generate_documentation(verilog_code: str, testbench: str) -> Dict[str, Any]:
    """Generate documentation for a Verilog design"""
    try:
        # Save the files temporarily
        temp_verilog = Path("mcp_output") / "temp.v"
        temp_tb = Path("mcp_output") / "temp_tb.sv"
        
        temp_verilog.write_text(verilog_code)
        temp_tb.write_text(testbench)
        
        # Generate documentation
        doc_results = verilog_agent.generate_documentation(temp_verilog, temp_tb)
        
        # Clean up
        temp_verilog.unlink()
        temp_tb.unlink()
        
        return doc_results
    except Exception as e:
        logger.error(f"Documentation generation failed: {str(e)}")
        raise

# FastAPI endpoints
@app.post("/design/generate", response_model=DesignResponse)
async def api_generate_design(request: DesignRequest) -> Dict[str, Any]:
    """Generate a complete Verilog design using the AI Agent"""
    return await generate_design(request.description, request.module_name)

@app.get("/design/{design_id}")
async def api_get_design(design_id: str) -> Dict[str, Any]:
    """Retrieve a previously generated design"""
    return await get_design(design_id)

@app.post("/design/optimize")
async def api_optimize_design(verilog_code: str) -> Dict[str, Any]:
    """Optimize an existing Verilog design"""
    return await optimize_design(verilog_code)

@app.post("/design/verify")
async def api_verify_design(verilog_code: str, testbench: str) -> Dict[str, Any]:
    """Verify a Verilog design"""
    return await verify_design(verilog_code, testbench)

@app.post("/design/document")
async def api_generate_documentation(verilog_code: str, testbench: str) -> Dict[str, Any]:
    """Generate documentation for a Verilog design"""
    return await generate_documentation(verilog_code, testbench)

async def main():
    """Main entry point for the MCP server"""
    try:
        # Create output directory
        Path("mcp_output").mkdir(exist_ok=True)
        
        # Start MCP server
        server_params = StdioServerParameters(
            command="python",
            args=["mcp_server.py"],
            env=None,
        )
        
        async with stdio_server(server_params) as (read, write):
            await server.serve(read, write)
            
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 