#!/usr/bin/env python3
"""
Documentation Generator for Verilog Designs
Generates comprehensive documentation including diagrams, specifications, and usage guides.
"""

import re
import json
from pathlib import Path
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import markdown
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ModuleDoc:
    """Documentation for a Verilog module."""
    name: str
    description: str
    parameters: List[Dict[str, str]]
    ports: List[Dict[str, str]]
    signals: List[Dict[str, str]]
    timing_diagrams: List[str]
    examples: List[str]

class DocGenerator:
    def __init__(self, verilog_file: str, testbench_file: str):
        """Initialize the documentation generator."""
        self.verilog_file = Path(verilog_file)
        self.testbench_file = Path(testbench_file)
        self.verilog_content = self.verilog_file.read_text()
        self.testbench_content = self.testbench_file.read_text()

    def extract_module_info(self) -> ModuleDoc:
        """Extract module information from Verilog code."""
        # Extract module name
        module_match = re.search(r'module\s+(\w+)', self.verilog_content)
        module_name = module_match.group(1) if module_match else "Unknown"

        # Extract module description from comments
        desc_match = re.search(r'/\*\*(.*?)\*/', self.verilog_content, re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else "No description available"

        # Extract parameters
        parameters = []
        param_matches = re.finditer(r'parameter\s+(\w+)\s*=\s*([^;]+);(?:\s*//\s*(.*))?', self.verilog_content)
        for match in param_matches:
            parameters.append({
                "name": match.group(1),
                "value": match.group(2).strip(),
                "description": match.group(3).strip() if match.group(3) else "No description"
            })

        # Extract ports
        ports = []
        port_matches = re.finditer(r'(input|output|inout)\s+(?:wire|reg)?\s*(?:\[([^\]]+)\])?\s*(\w+)(?:\s*//\s*(.*))?', self.verilog_content)
        for match in port_matches:
            ports.append({
                "direction": match.group(1),
                "width": match.group(2) if match.group(2) else "1",
                "name": match.group(3),
                "description": match.group(4).strip() if match.group(4) else "No description"
            })

        # Extract internal signals
        signals = []
        signal_matches = re.finditer(r'(wire|reg)\s*(?:\[([^\]]+)\])?\s*(\w+)(?:\s*//\s*(.*))?', self.verilog_content)
        for match in signal_matches:
            signals.append({
                "type": match.group(1),
                "width": match.group(2) if match.group(2) else "1",
                "name": match.group(3),
                "description": match.group(4).strip() if match.group(4) else "No description"
            })

        # Generate timing diagrams (placeholder)
        timing_diagrams = [
            "```wavedrom\n{signal: [\n  {name: 'clk', wave: 'p....'},\n  {name: 'data', wave: 'x345x'},\n]}\n```"
        ]

        # Extract examples from testbench
        examples = []
        example_matches = re.finditer(r'// Test case.*?\n(.*?)// End test case', self.testbench_content, re.DOTALL)
        for match in example_matches:
            examples.append(match.group(1).strip())

        return ModuleDoc(
            name=module_name,
            description=description,
            parameters=parameters,
            ports=ports,
            signals=signals,
            timing_diagrams=timing_diagrams,
            examples=examples
        )

    def generate_markdown_doc(self, module_doc: ModuleDoc) -> str:
        """Generate markdown documentation."""
        doc = []

        # Title and Description
        doc.append(f"# {module_doc.name}")
        doc.append(f"\n{module_doc.description}\n")

        # Parameters
        if module_doc.parameters:
            doc.append("## Parameters")
            doc.append("\n| Parameter | Value | Description |")
            doc.append("|-----------|--------|-------------|")
            for param in module_doc.parameters:
                doc.append(f"| {param['name']} | {param['value']} | {param['description']} |")
            doc.append("")

        # Ports
        if module_doc.ports:
            doc.append("## Ports")
            doc.append("\n| Port | Direction | Width | Description |")
            doc.append("|------|-----------|--------|-------------|")
            for port in module_doc.ports:
                doc.append(f"| {port['name']} | {port['direction']} | {port['width']} | {port['description']} |")
            doc.append("")

        # Internal Signals
        if module_doc.signals:
            doc.append("## Internal Signals")
            doc.append("\n| Signal | Type | Width | Description |")
            doc.append("|--------|------|--------|-------------|")
            for signal in module_doc.signals:
                doc.append(f"| {signal['name']} | {signal['type']} | {signal['width']} | {signal['description']} |")
            doc.append("")

        # Timing Diagrams
        if module_doc.timing_diagrams:
            doc.append("## Timing Diagrams")
            for diagram in module_doc.timing_diagrams:
                doc.append(diagram)
            doc.append("")

        # Examples
        if module_doc.examples:
            doc.append("## Usage Examples")
            for i, example in enumerate(module_doc.examples, 1):
                doc.append(f"\n### Example {i}")
                doc.append("```verilog")
                doc.append(example)
                doc.append("```\n")

        return "\n".join(doc)

    def generate_html_doc(self, markdown_content: str) -> str:
        """Convert markdown to HTML."""
        return markdown.markdown(
            markdown_content,
            extensions=['tables', 'fenced_code', 'codehilite']
        )

    def generate_yaml_doc(self, module_doc: ModuleDoc) -> str:
        """Generate YAML documentation."""
        doc_dict = {
            "module": {
                "name": module_doc.name,
                "description": module_doc.description,
                "parameters": module_doc.parameters,
                "ports": module_doc.ports,
                "signals": module_doc.signals,
                "examples": module_doc.examples
            }
        }
        return yaml.dump(doc_dict, sort_keys=False, default_flow_style=False)

    def generate_all(self) -> Dict[str, str]:
        """Generate all documentation formats."""
        module_doc = self.extract_module_info()
        
        markdown_doc = self.generate_markdown_doc(module_doc)
        html_doc = self.generate_html_doc(markdown_doc)
        yaml_doc = self.generate_yaml_doc(module_doc)

        return {
            "markdown": markdown_doc,
            "html": html_doc,
            "yaml": yaml_doc
        }

def main():
    """Main entry point for the documentation generator."""
    try:
        # Initialize generator
        generator = DocGenerator(
            verilog_file="test_output/risc_processor.v",
            testbench_file="test_output/risc_processor_tb.sv"
        )

        # Generate documentation
        docs = generator.generate_all()

        # Save documentation files
        output_dir = Path("test_output/docs")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save Markdown
        markdown_file = output_dir / "documentation.md"
        markdown_file.write_text(docs["markdown"])
        logger.info(f"Markdown documentation generated: {markdown_file}")

        # Save HTML
        html_file = output_dir / "documentation.html"
        html_file.write_text(docs["html"])
        logger.info(f"HTML documentation generated: {html_file}")

        # Save YAML
        yaml_file = output_dir / "documentation.yaml"
        yaml_file.write_text(docs["yaml"])
        logger.info(f"YAML documentation generated: {yaml_file}")

    except Exception as e:
        logger.error(f"Documentation generation failed: {str(e)}")
        raise

if __name__ == "__main__":
    main() 