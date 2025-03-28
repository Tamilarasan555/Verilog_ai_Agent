#!/usr/bin/env python3
"""
Standalone Verilog Generator - Using DeepSeek Function Calling for enhanced analysis
"""

import os
import json
import re
import argparse
import asyncio
from pathlib import Path
import logging
from typing import Dict, Any, Optional, Tuple, List
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VerilogGenerator:
    def __init__(self):
        """Initialize the Verilog generator with API configurations."""
        # Configure DeepSeek
        self.client = openai.AsyncOpenAI(
            api_key=os.getenv('DEEPSEEK_API_KEY'),
            base_url="https://api.deepseek.com/v1"
        )
        
        # Define function tools for Verilog generation
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "analyze_verilog_design",
                    "description": "Analyze a Verilog design description and create a structured design plan",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "module_name": {
                                "type": "string",
                                "description": "Name of the Verilog module"
                            },
                            "description": {
                                "type": "string",
                                "description": "Detailed description of the module's functionality"
                            },
                            "design_type": {
                                "type": "string",
                                "enum": ["combinational", "sequential", "fsm", "memory", "datapath", "control", "interface", "other"],
                                "description": "Type of Verilog design"
                            },
                            "ports": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "direction": {"type": "string", "enum": ["input", "output", "inout"]},
                                        "width": {"type": "string"},
                                        "type": {"type": "string", "enum": ["wire", "reg", "integer", "real", "time"]},
                                        "description": {"type": "string"},
                                        "is_clock": {"type": "boolean"},
                                        "is_reset": {"type": "boolean"},
                                        "is_enable": {"type": "boolean"}
                                    },
                                    "required": ["name", "direction", "width", "type", "description"]
                                }
                            },
                            "parameters": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "value": {"type": "string"},
                                        "type": {"type": "string", "enum": ["integer", "real", "string"]},
                                        "description": {"type": "string"}
                                    },
                                    "required": ["name", "value", "type", "description"]
                                }
                            },
                            "internal_signals": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "width": {"type": "string"},
                                        "type": {"type": "string", "enum": ["wire", "reg", "integer", "real", "time"]},
                                        "description": {"type": "string"}
                                    },
                                    "required": ["name", "width", "type", "description"]
                                }
                            },
                            "timing_constraints": {
                                "type": "object",
                                "properties": {
                                    "clock_period": {"type": "string"},
                                    "setup_time": {"type": "string"},
                                    "hold_time": {"type": "string"},
                                    "max_delay": {"type": "string"},
                                    "min_delay": {"type": "string"}
                                }
                            },
                            "design_constraints": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of design constraints and requirements"
                            }
                        },
                        "required": ["module_name", "description", "design_type", "ports", "parameters"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_verilog_code",
                    "description": "Generate Verilog code for a given design plan",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "module_code": {
                                "type": "string",
                                "description": "The complete Verilog module code"
                            },
                            "implementation_details": {
                                "type": "object",
                                "properties": {
                                    "architecture": {"type": "string"},
                                    "state_machine": {
                                        "type": "object",
                                        "properties": {
                                            "states": {"type": "array", "items": {"type": "string"}},
                                            "transitions": {"type": "array", "items": {"type": "string"}}
                                        }
                                    },
                                    "datapath": {
                                        "type": "object",
                                        "properties": {
                                            "components": {"type": "array", "items": {"type": "string"}},
                                            "dataflow": {"type": "string"}
                                        }
                                    }
                                }
                            },
                            "comments": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of important comments about the implementation"
                            },
                            "synthesis_guidelines": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of synthesis-specific guidelines and considerations"
                            }
                        },
                        "required": ["module_code", "implementation_details", "comments"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_testbench",
                    "description": "Generate a SystemVerilog testbench for a given Verilog module",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "testbench_code": {
                                "type": "string",
                                "description": "The complete SystemVerilog testbench code"
                            },
                            "test_scenarios": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "description": {"type": "string"},
                                        "stimulus": {"type": "string"},
                                        "expected_result": {"type": "string"},
                                        "coverage_points": {"type": "array", "items": {"type": "string"}}
                                    },
                                    "required": ["name", "description", "stimulus", "expected_result"]
                                }
                            },
                            "coverage_plan": {
                                "type": "object",
                                "properties": {
                                    "functional_coverage": {"type": "array", "items": {"type": "string"}},
                                    "code_coverage": {"type": "array", "items": {"type": "string"}},
                                    "assertions": {"type": "array", "items": {"type": "string"}}
                                }
                            },
                            "debug_features": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of debug features included in the testbench"
                            }
                        },
                        "required": ["testbench_code", "test_scenarios", "coverage_plan"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "validate_verilog_code",
                    "description": "Validate Verilog code and check for potential issues",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "warnings": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "severity": {"type": "string", "enum": ["low", "medium", "high"]},
                                        "message": {"type": "string"},
                                        "location": {"type": "string"},
                                        "suggestion": {"type": "string"}
                                    },
                                    "required": ["severity", "message", "location"]
                                }
                            },
                            "suggestions": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "category": {"type": "string", "enum": ["synthesis", "simulation", "timing", "style", "maintainability"]},
                                        "message": {"type": "string"},
                                        "impact": {"type": "string"},
                                        "implementation": {"type": "string"}
                                    },
                                    "required": ["category", "message", "impact"]
                                }
                            },
                            "verification_metrics": {
                                "type": "object",
                                "properties": {
                                    "code_complexity": {"type": "string"},
                                    "test_coverage": {"type": "string"},
                                    "synthesis_quality": {"type": "string"}
                                }
                            }
                        },
                        "required": ["warnings", "suggestions", "verification_metrics"]
                    }
                }
            }
        ]

    async def send_messages(self, messages: List[Dict[str, str]], tools: Optional[List[Dict]] = None) -> Dict:
        """Send messages to the API and handle function calls."""
        try:
            response = await self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                tools=tools if tools else self.tools
            )
            return response.choices[0].message
        except Exception as e:
            logger.error(f"API call failed: {str(e)}")
            raise

    async def analyze_design(self, description: str) -> Dict[str, Any]:
        """Stage 1: Analyze the design description and create a structured plan."""
        try:
            messages = [{"role": "user", "content": f"Analyze this Verilog design description and create a structured design plan:\n\n{description}"}]
            message = await self.send_messages(messages)
            
            if message.tool_calls:
                tool_call = message.tool_calls[0]
                if tool_call.function.name == "analyze_verilog_design":
                    design_plan = json.loads(tool_call.function.arguments)
                    logger.info(f"Generated design plan for module: {design_plan['module_name']}")
                    logger.info(f"Design type: {design_plan['design_type']}")
                    return design_plan
            
            raise ValueError("No valid design plan generated")
                
        except Exception as e:
            logger.error(f"Failed to analyze design: {str(e)}")
            raise

    async def generate_verilog(self, design_plan: Dict[str, Any]) -> str:
        """Stage 2: Generate Verilog code from the design plan."""
        try:
            messages = [
                {"role": "user", "content": f"Generate Verilog code for this design plan:\n\n{json.dumps(design_plan, indent=2)}"}
            ]
            message = await self.send_messages(messages)
            
            if message.tool_calls:
                tool_call = message.tool_calls[0]
                if tool_call.function.name == "generate_verilog_code":
                    result = json.loads(tool_call.function.arguments)
                    verilog_code = result["module_code"]
                    logger.info("Implementation details:\n%s", json.dumps(result["implementation_details"], indent=2))
                    logger.info("Implementation comments:\n%s", "\n".join(result["comments"]))
                    if result.get("synthesis_guidelines"):
                        logger.info("Synthesis guidelines:\n%s", "\n".join(result["synthesis_guidelines"]))
                    return verilog_code
            
            raise ValueError("No valid Verilog code generated")
            
        except Exception as e:
            logger.error(f"Failed to generate Verilog code: {str(e)}")
            raise

    async def generate_testbench(self, verilog_code: str, module_name: str) -> str:
        """Stage 3: Generate a testbench for the Verilog module."""
        try:
            messages = [
                {"role": "user", "content": f"Generate a SystemVerilog testbench for this Verilog module:\n\n{verilog_code}"}
            ]
            message = await self.send_messages(messages)
            
            if message.tool_calls:
                tool_call = message.tool_calls[0]
                if tool_call.function.name == "generate_testbench":
                    result = json.loads(tool_call.function.arguments)
                    testbench_code = result["testbench_code"]
                    logger.info("Test scenarios:\n%s", json.dumps(result["test_scenarios"], indent=2))
                    logger.info("Coverage plan:\n%s", json.dumps(result["coverage_plan"], indent=2))
                    if result.get("debug_features"):
                        logger.info("Debug features:\n%s", "\n".join(result["debug_features"]))
                    return testbench_code
            
            raise ValueError("No valid testbench generated")
            
        except Exception as e:
            logger.error(f"Failed to generate testbench: {str(e)}")
            raise

    async def validate_code(self, verilog_code: str, testbench_code: Optional[str] = None) -> List[str]:
        """Stage 4: Validate the generated code and check for potential issues."""
        try:
            messages = [
                {"role": "user", "content": f"Validate this Verilog code and testbench:\n\nVerilog:\n{verilog_code}\n\nTestbench:\n{testbench_code if testbench_code else 'None'}"}
            ]
            message = await self.send_messages(messages)
            
            if message.tool_calls:
                tool_call = message.tool_calls[0]
                if tool_call.function.name == "validate_verilog_code":
                    result = json.loads(tool_call.function.arguments)
                    warnings = result["warnings"]
                    suggestions = result["suggestions"]
                    metrics = result["verification_metrics"]
                    
                    logger.info("Verification metrics:\n%s", json.dumps(metrics, indent=2))
                    logger.info("Improvement suggestions:\n%s", json.dumps(suggestions, indent=2))
                    
                    # Format warnings with severity
                    formatted_warnings = []
                    for warning in warnings:
                        formatted_warnings.append(f"[{warning['severity'].upper()}] {warning['message']} at {warning['location']}")
                        if warning.get("suggestion"):
                            formatted_warnings.append(f"  Suggestion: {warning['suggestion']}")
                    
                    return formatted_warnings
            
            return []
            
        except Exception as e:
            logger.error(f"Failed to validate code: {str(e)}")
            return []

    async def generate(self, description: str, output_dir: str, module_name: Optional[str] = None, generate_testbench: bool = False) -> None:
        """Main generation pipeline that orchestrates all stages."""
        try:
            # Create output directory if it doesn't exist
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Stage 1: Design Analysis
            design_plan = await self.analyze_design(description)
            
            # Override module name if specified
            if module_name:
                design_plan['module_name'] = module_name
            
            # Stage 2: Code Generation
            verilog_code = await self.generate_verilog(design_plan)
            
            # Write Verilog module
            module_file = output_path / f"{design_plan['module_name']}.v"
            module_file.write_text(verilog_code)
            logger.info(f"Verilog module written to: {module_file}")
            
            # Stage 3: Testbench Generation (if requested)
            testbench_code = None
            if generate_testbench:
                testbench_code = await self.generate_testbench(verilog_code, design_plan['module_name'])
                testbench_file = output_path / f"{design_plan['module_name']}_tb.sv"
                testbench_file.write_text(testbench_code)
                logger.info(f"Testbench written to: {testbench_file}")
            
            # Stage 4: Quality Assurance
            warnings = await self.validate_code(verilog_code, testbench_code)
            if warnings:
                warnings_file = output_path / f"{design_plan['module_name']}_warnings.txt"
                warnings_file.write_text("\n".join(warnings))
                logger.info(f"Warnings written to: {warnings_file}")
            
            logger.info("Generation completed successfully!")
            
        except Exception as e:
            logger.error(f"Generation failed: {str(e)}")
            raise

async def main():
    """Main entry point for the Verilog generator."""
    parser = argparse.ArgumentParser(description='Generate Verilog code from natural language descriptions')
    parser.add_argument('-d', '--description', help='Design description')
    parser.add_argument('-f', '--file', help='File containing design description')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('-m', '--module-name', help='Specify module name')
    parser.add_argument('-t', '--testbench', action='store_true', help='Generate testbench')
    
    args = parser.parse_args()
    
    if not args.description and not args.file:
        parser.error("Either --description or --file must be provided")
    
    description = args.description
    if args.file:
        with open(args.file, 'r') as f:
            description = f.read().strip()
    
    generator = VerilogGenerator()
    await generator.generate(
        description=description,
        output_dir=args.output,
        module_name=args.module_name,
        generate_testbench=args.testbench
    )

if __name__ == "__main__":
    asyncio.run(main()) 