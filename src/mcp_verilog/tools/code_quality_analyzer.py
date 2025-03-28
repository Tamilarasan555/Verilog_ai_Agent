#!/usr/bin/env python3
"""
Code Quality Analyzer and Improver for Generated RISC Processor
"""

import os
import re
import json
from pathlib import Path
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComponentType(Enum):
    """Enum for different types of components in the RISC processor."""
    ALU = "ALU"
    REGISTER_FILE = "Register File"
    CACHE = "Cache"
    CONTROL_UNIT = "Control Unit"
    PIPELINE_STAGE = "Pipeline Stage"
    DEBUG_INTERFACE = "Debug Interface"

@dataclass
class ComponentAnalysis:
    """Data class to store analysis results for each component."""
    component_type: ComponentType
    is_implemented: bool
    implementation_level: str  # "full", "partial", "simplified", "missing"
    issues: List[str]
    suggestions: List[str]

class CodeQualityAnalyzer:
    def __init__(self, verilog_file: str, testbench_file: str):
        """Initialize the analyzer with paths to Verilog and testbench files."""
        self.verilog_file = Path(verilog_file)
        self.testbench_file = Path(testbench_file)
        self.verilog_content = self.verilog_file.read_text()
        self.testbench_content = self.testbench_file.read_text()
        self.analysis_results: Dict[ComponentType, ComponentAnalysis] = {}

    def analyze_module_structure(self) -> List[str]:
        """Analyze the overall module structure."""
        issues = []
        suggestions = []

        # Check for parameter definitions
        if not re.search(r'parameter\s+\w+\s*=\s*\d+', self.verilog_content):
            issues.append("Missing parameter definitions")
            suggestions.append("Add parameter definitions for cache sizes, register count, etc.")

        # Check for port declarations
        if not re.search(r'input\s+wire\s+clk', self.verilog_content):
            issues.append("Missing clock port")
            suggestions.append("Add clock port declaration")

        # Check for debug interface
        if not re.search(r'debug_\w+', self.verilog_content):
            issues.append("Incomplete debug interface")
            suggestions.append("Add comprehensive debug interface with monitoring signals")

        return issues, suggestions

    def analyze_alu(self) -> ComponentAnalysis:
        """Analyze ALU implementation."""
        issues = []
        suggestions = []

        # Check for ALU operation codes
        if not re.search(r'case\s*\(.*op.*\)', self.verilog_content):
            issues.append("Missing ALU operation codes")
            suggestions.append("Implement full ALU with all required operations")

        # Check for ALU flags
        if not re.search(r'zero|carry|overflow', self.verilog_content):
            issues.append("Missing ALU flags")
            suggestions.append("Add ALU flags for zero, carry, and overflow conditions")

        return ComponentAnalysis(
            component_type=ComponentType.ALU,
            is_implemented=True,
            implementation_level="simplified",
            issues=issues,
            suggestions=suggestions
        )

    def analyze_register_file(self) -> ComponentAnalysis:
        """Analyze register file implementation."""
        issues = []
        suggestions = []

        # Check for register file implementation
        if not re.search(r'reg\s+\[.*\]\s+reg_file', self.verilog_content):
            issues.append("Missing register file implementation")
            suggestions.append("Implement 32-register file with read/write ports")

        # Check for register file control
        if not re.search(r'reg_write|reg_read', self.verilog_content):
            issues.append("Missing register file control signals")
            suggestions.append("Add register file control signals and logic")

        return ComponentAnalysis(
            component_type=ComponentType.REGISTER_FILE,
            is_implemented=False,
            implementation_level="missing",
            issues=issues,
            suggestions=suggestions
        )

    def analyze_cache(self) -> ComponentAnalysis:
        """Analyze cache implementation."""
        issues = []
        suggestions = []

        # Check for cache implementation
        if not re.search(r'cache_\w+', self.verilog_content):
            issues.append("Missing cache implementation")
            suggestions.append("Implement instruction and data caches")

        # Check for cache control
        if not re.search(r'cache_hit|cache_miss', self.verilog_content):
            issues.append("Missing cache control signals")
            suggestions.append("Add cache hit/miss detection and handling")

        return ComponentAnalysis(
            component_type=ComponentType.CACHE,
            is_implemented=False,
            implementation_level="missing",
            issues=issues,
            suggestions=suggestions
        )

    def analyze_pipeline_stages(self) -> ComponentAnalysis:
        """Analyze pipeline stage implementation."""
        issues = []
        suggestions = []

        # Check for all pipeline stages
        stages = ["IF", "ID", "EX", "MEM", "WB"]
        for stage in stages:
            if not re.search(rf'{stage.lower()}_\w+', self.verilog_content):
                issues.append(f"Missing {stage} stage implementation")
                suggestions.append(f"Implement complete {stage} stage with proper control")

        # Check for pipeline registers
        if not re.search(r'@\(posedge\s+clk\)', self.verilog_content):
            issues.append("Missing pipeline registers")
            suggestions.append("Add pipeline registers between stages")

        return ComponentAnalysis(
            component_type=ComponentType.PIPELINE_STAGE,
            is_implemented=True,
            implementation_level="partial",
            issues=issues,
            suggestions=suggestions
        )

    def analyze_testbench(self) -> List[str]:
        """Analyze testbench coverage and quality."""
        issues = []
        suggestions = []

        # Check for test scenarios
        if not re.search(r'Test case \d+:', self.testbench_content):
            issues.append("Limited test scenarios")
            suggestions.append("Add more comprehensive test scenarios")

        # Check for assertions
        if not re.search(r'assert|property', self.testbench_content):
            issues.append("Missing assertions")
            suggestions.append("Add SystemVerilog assertions for pipeline stages")

        # Check for coverage points
        if not re.search(r'covergroup|coverpoint', self.testbench_content):
            issues.append("Missing coverage points")
            suggestions.append("Add functional and code coverage points")

        return issues, suggestions

    def analyze_all(self) -> Dict[str, Any]:
        """Perform comprehensive analysis of the code."""
        analysis_results = {
            "module_structure": {
                "issues": [],
                "suggestions": []
            },
            "components": {},
            "testbench": {
                "issues": [],
                "suggestions": []
            }
        }

        # Analyze module structure
        analysis_results["module_structure"]["issues"], \
        analysis_results["module_structure"]["suggestions"] = self.analyze_module_structure()

        # Analyze components
        analysis_results["components"]["alu"] = self.analyze_alu()
        analysis_results["components"]["register_file"] = self.analyze_register_file()
        analysis_results["components"]["cache"] = self.analyze_cache()
        analysis_results["components"]["pipeline_stages"] = self.analyze_pipeline_stages()

        # Analyze testbench
        analysis_results["testbench"]["issues"], \
        analysis_results["testbench"]["suggestions"] = self.analyze_testbench()

        return analysis_results

    def generate_improvement_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate a detailed improvement report."""
        report = []
        report.append("=== RISC Processor Code Quality Analysis Report ===\n")

        # Module Structure
        report.append("1. Module Structure Analysis:")
        for issue in analysis_results["module_structure"]["issues"]:
            report.append(f"   - Issue: {issue}")
        for suggestion in analysis_results["module_structure"]["suggestions"]:
            report.append(f"   - Suggestion: {suggestion}")
        report.append("")

        # Components
        report.append("2. Component Analysis:")
        for component_name, analysis in analysis_results["components"].items():
            report.append(f"\n   {component_name.upper()}:")
            report.append(f"   - Implementation Level: {analysis.implementation_level}")
            for issue in analysis.issues:
                report.append(f"   - Issue: {issue}")
            for suggestion in analysis.suggestions:
                report.append(f"   - Suggestion: {suggestion}")

        # Testbench
        report.append("\n3. Testbench Analysis:")
        for issue in analysis_results["testbench"]["issues"]:
            report.append(f"   - Issue: {issue}")
        for suggestion in analysis_results["testbench"]["suggestions"]:
            report.append(f"   - Suggestion: {suggestion}")

        return "\n".join(report)

def main():
    """Main entry point for the code quality analyzer."""
    try:
        # Initialize analyzer
        analyzer = CodeQualityAnalyzer(
            verilog_file="test_output/risc_processor.v",
            testbench_file="test_output/risc_processor_tb.sv"
        )

        # Perform analysis
        analysis_results = analyzer.analyze_all()

        # Generate and save report
        report = analyzer.generate_improvement_report(analysis_results)
        report_file = Path("test_output/code_quality_report.txt")
        report_file.write_text(report)
        logger.info(f"Code quality report generated: {report_file}")

    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise

if __name__ == "__main__":
    main() 