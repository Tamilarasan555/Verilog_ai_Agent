#!/usr/bin/env python3
"""
Verilog AI Agent - Main Orchestrator
Coordinates all components for Verilog code generation, optimization, verification, and documentation.
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from verilog_generator import VerilogGenerator
from design_optimizer import DesignOptimizer
from design_verifier import DesignVerifier
from doc_generator import DocGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VerilogAIAgent:
    def __init__(self, output_dir: str = "test_output"):
        """Initialize the AI agent."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.generator = VerilogGenerator()

    async def generate_design(self, description: str, module_name: Optional[str] = None) -> Dict[str, Path]:
        """Generate Verilog design and testbench."""
        logger.info("Stage 1: Generating Verilog design...")
        
        # Generate Verilog code and testbench
        await self.generator.generate(
            description=description,
            output_dir=str(self.output_dir),
            module_name=module_name,
            generate_testbench=True
        )

        # Get file paths
        verilog_file = self.output_dir / f"{module_name or 'design'}.v"
        testbench_file = self.output_dir / f"{module_name or 'design'}_tb.sv"

        return {
            "verilog": verilog_file,
            "testbench": testbench_file
        }

    def optimize_design(self, verilog_file: Path) -> Dict[str, Any]:
        """Optimize the generated design."""
        logger.info("Stage 2: Optimizing design...")
        
        # Initialize optimizer
        optimizer = DesignOptimizer(str(verilog_file))
        
        # Perform optimization
        optimization_report = optimizer.optimize_all()
        
        # Apply optimizations
        optimized_code = optimizer.apply_optimizations(optimization_report)
        
        # Save optimized code
        optimized_file = self.output_dir / f"{verilog_file.stem}_optimized.v"
        optimized_file.write_text(optimized_code)
        
        return {
            "report": optimization_report,
            "optimized_file": optimized_file
        }

    def verify_design(self, verilog_file: Path, testbench_file: Path) -> Dict[str, Any]:
        """Verify the design."""
        logger.info("Stage 3: Verifying design...")
        
        # Initialize verifier
        verifier = DesignVerifier(str(verilog_file), str(testbench_file))
        
        # Perform verification
        verification_report = verifier.verify_all()
        
        # Generate assertions and coverage
        assertions = verifier.generate_assertions()
        coverage_model = verifier.generate_coverage_model()
        
        # Save generated files
        assertions_file = self.output_dir / f"{verilog_file.stem}_assertions.sv"
        coverage_file = self.output_dir / f"{verilog_file.stem}_coverage.sv"
        
        assertions_file.write_text(assertions)
        coverage_file.write_text(coverage_model)
        
        return {
            "report": verification_report,
            "assertions_file": assertions_file,
            "coverage_file": coverage_file
        }

    def generate_documentation(self, verilog_file: Path, testbench_file: Path) -> Dict[str, Path]:
        """Generate documentation."""
        logger.info("Stage 4: Generating documentation...")
        
        # Initialize documentation generator
        doc_gen = DocGenerator(str(verilog_file), str(testbench_file))
        
        # Generate documentation
        docs = doc_gen.generate_all()
        
        # Create docs directory
        docs_dir = self.output_dir / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        # Save documentation files
        doc_files = {}
        for format_name, content in docs.items():
            file_path = docs_dir / f"documentation.{format_name}"
            file_path.write_text(content)
            doc_files[format_name] = file_path
        
        return doc_files

    async def process_design(self, description: str, module_name: Optional[str] = None) -> Dict[str, Any]:
        """Process the entire design pipeline."""
        try:
            # Stage 1: Generate Design
            files = await self.generate_design(description, module_name)
            logger.info(f"Design generated: {files['verilog']}")
            logger.info(f"Testbench generated: {files['testbench']}")

            # Stage 2: Optimize Design
            optimization_results = self.optimize_design(files["verilog"])
            logger.info(f"Design optimized: {optimization_results['optimized_file']}")

            # Stage 3: Verify Design
            verification_results = self.verify_design(
                optimization_results["optimized_file"],
                files["testbench"]
            )
            logger.info("Design verification completed")

            # Stage 4: Generate Documentation
            documentation_files = self.generate_documentation(
                optimization_results["optimized_file"],
                files["testbench"]
            )
            logger.info("Documentation generated")

            # Prepare final report
            return {
                "files": {
                    "original": files,
                    "optimized": optimization_results["optimized_file"],
                    "verification": {
                        "assertions": verification_results["assertions_file"],
                        "coverage": verification_results["coverage_file"]
                    },
                    "documentation": documentation_files
                },
                "reports": {
                    "optimization": optimization_results["report"],
                    "verification": verification_results["report"]
                }
            }

        except Exception as e:
            logger.error(f"Design processing failed: {str(e)}")
            raise

async def main():
    """Main entry point for the Verilog AI Agent."""
    try:
        # Initialize agent
        agent = VerilogAIAgent()

        # Process RISC processor design
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

        # Process the design
        results = await agent.process_design(description, "risc_processor")
        
        # Log results
        logger.info("Design processing completed successfully!")
        logger.info(f"Generated files:")
        for category, files in results["files"].items():
            if isinstance(files, dict):
                for file_type, file_path in files.items():
                    logger.info(f"  - {category}/{file_type}: {file_path}")
            else:
                logger.info(f"  - {category}: {files}")

    except Exception as e:
        logger.error(f"AI Agent failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 