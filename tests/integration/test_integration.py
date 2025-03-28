import asyncio
import httpx
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/test_integration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Test configuration
TEST_CONFIG = {
    'server_url': 'http://localhost:8000',
    'timeout': 30
}

async def test_server_connection():
    """Test basic server connectivity"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{TEST_CONFIG['server_url']}/health")
            assert response.status_code == 200
            logger.info("Server connection test passed")
        except Exception as e:
            logger.error(f"Server connection test failed: {str(e)}")
            raise

async def test_verilog_generation():
    """Test Verilog code generation through the API"""
    test_data = {
        "module_name": "test_module",
        "ports": [
            {"name": "clk", "direction": "input", "width": 1},
            {"name": "rst_n", "direction": "input", "width": 1},
            {"name": "data_out", "direction": "output", "width": 8}
        ]
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{TEST_CONFIG['server_url']}/generate",
                json=test_data,
                timeout=TEST_CONFIG['timeout']
            )
            assert response.status_code == 200
            result = response.json()
            assert "verilog_code" in result
            logger.info("Verilog generation test passed")
        except Exception as e:
            logger.error(f"Verilog generation test failed: {str(e)}")
            raise

async def test_design_optimization():
    """Test design optimization through the API"""
    test_data = {
        "verilog_code": """
        module test_module (
            input clk,
            input rst_n,
            output reg [7:0] data_out
        );
            always @(posedge clk or negedge rst_n) begin
                if (!rst_n)
                    data_out <= 8'h00;
                else
                    data_out <= data_out + 1;
            end
        endmodule
        """
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{TEST_CONFIG['server_url']}/optimize",
                json=test_data,
                timeout=TEST_CONFIG['timeout']
            )
            assert response.status_code == 200
            result = response.json()
            assert "optimized_code" in result
            logger.info("Design optimization test passed")
        except Exception as e:
            logger.error(f"Design optimization test failed: {str(e)}")
            raise

async def main():
    """Run all integration tests"""
    tests = [
        test_server_connection,
        test_verilog_generation,
        test_design_optimization
    ]
    
    for test in tests:
        try:
            await test()
        except Exception as e:
            logger.error(f"Test {test.__name__} failed: {str(e)}")
            raise

if __name__ == "__main__":
    asyncio.run(main()) 