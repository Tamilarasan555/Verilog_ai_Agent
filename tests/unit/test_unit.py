#!/usr/bin/env python3
"""
Test script for Verilog Generator with complex design examples
"""

import asyncio
import logging
from pathlib import Path
import pytest
from mcp_verilog.tools.verilog_generator import VerilogGenerator
from mcp_verilog.tools.design_optimizer import DesignOptimizer
from mcp_verilog.tools.design_verifier import DesignVerifier

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/test_unit.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@pytest.fixture
def verilog_generator():
    """Fixture for VerilogGenerator instance"""
    return VerilogGenerator()

@pytest.fixture
def design_optimizer():
    """Fixture for DesignOptimizer instance"""
    return DesignOptimizer()

@pytest.fixture
def design_verifier():
    """Fixture for DesignVerifier instance"""
    return DesignVerifier()

def test_verilog_generator_basic(verilog_generator):
    """Test basic Verilog code generation"""
    module_name = "test_module"
    ports = [
        {"name": "clk", "direction": "input", "width": 1},
        {"name": "rst_n", "direction": "input", "width": 1},
        {"name": "data_out", "direction": "output", "width": 8}
    ]
    
    verilog_code = verilog_generator.generate_module(module_name, ports)
    assert "module test_module" in verilog_code
    assert "input clk" in verilog_code
    assert "input rst_n" in verilog_code
    assert "output [7:0] data_out" in verilog_code

def test_design_optimizer_basic(design_optimizer):
    """Test basic design optimization"""
    test_code = """
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
    
    optimized_code = design_optimizer.optimize(test_code)
    assert "module test_module" in optimized_code
    assert "input clk" in optimized_code
    assert "input rst_n" in optimized_code
    assert "output reg [7:0] data_out" in optimized_code

def test_design_verifier_basic(design_verifier):
    """Test basic design verification"""
    test_code = """
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
    
    verification_result = design_verifier.verify(test_code)
    assert verification_result["is_valid"]
    assert "syntax_check" in verification_result
    assert "timing_check" in verification_result

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 