#!/usr/bin/env python3
"""
Design Verifier for Verilog Code
Performs formal verification, assertion checking, and coverage analysis.
"""

import re
import json
from pathlib import Path
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VerificationType(Enum):
    """Types of verification that can be performed."""
    FORMAL = "formal"
    FUNCTIONAL = "functional"
    ASSERTION = "assertion"
    COVERAGE = "coverage"

@dataclass
class VerificationResult:
    """Results of verification analysis."""
    verification_type: VerificationType
    passed: bool
    coverage: float
    issues: List[str]
    suggestions: List[str]

class DesignVerifier:
    def __init__(self, verilog_file: str, testbench_file: str):
        """Initialize the design verifier."""
        self.verilog_file = Path(verilog_file)
        self.testbench_file = Path(testbench_file)
        self.verilog_content = self.verilog_file.read_text()
        self.testbench_content = self.testbench_file.read_text()
        self.verification_results: Dict[VerificationType, VerificationResult] = {}

    def verify_formal_properties(self) -> VerificationResult:
        """Verify formal properties of the design."""
        issues = []
        suggestions = []
        coverage = 0.0

        # Check for formal properties
        if not re.search(r'property\s+\w+', self.verilog_content):
            issues.append("No formal properties defined")
            suggestions.append("Add SVA properties for critical behavior")
            coverage = 0.0
        else:
            property_count = len(re.findall(r'property\s+\w+', self.verilog_content))
            coverage = min(100.0, property_count * 20.0)  # 20% per property, max 100%

        # Check for assumptions
        if not re.search(r'assume\s+\w+', self.verilog_content):
            issues.append("No assumptions defined")
            suggestions.append("Add assumptions about input behavior")

        return VerificationResult(
            verification_type=VerificationType.FORMAL,
            passed=len(issues) == 0,
            coverage=coverage,
            issues=issues,
            suggestions=suggestions
        )

    def verify_functional_coverage(self) -> VerificationResult:
        """Verify functional coverage of the design."""
        issues = []
        suggestions = []
        coverage = 0.0

        # Check for covergroups
        if not re.search(r'covergroup\s+\w+', self.testbench_content):
            issues.append("No coverage groups defined")
            suggestions.append("Add covergroups for functional coverage")
        else:
            covergroup_count = len(re.findall(r'covergroup\s+\w+', self.testbench_content))
            coverage = min(100.0, covergroup_count * 25.0)  # 25% per covergroup, max 100%

        # Check for coverage points
        if not re.search(r'coverpoint\s+\w+', self.testbench_content):
            issues.append("No coverage points defined")
            suggestions.append("Add coverage points for state space exploration")

        return VerificationResult(
            verification_type=VerificationType.FUNCTIONAL,
            passed=len(issues) == 0,
            coverage=coverage,
            issues=issues,
            suggestions=suggestions
        )

    def verify_assertions(self) -> VerificationResult:
        """Verify assertions in the design."""
        issues = []
        suggestions = []
        coverage = 0.0

        # Check for assertions
        if not re.search(r'assert\s+\w+', self.testbench_content):
            issues.append("No assertions defined")
            suggestions.append("Add assertions for design invariants")
        else:
            assertion_count = len(re.findall(r'assert\s+\w+', self.testbench_content))
            coverage = min(100.0, assertion_count * 10.0)  # 10% per assertion, max 100%

        # Check for temporal assertions
        if not re.search(r'##\d+|@\(posedge', self.testbench_content):
            issues.append("No temporal assertions defined")
            suggestions.append("Add temporal assertions for sequential behavior")

        return VerificationResult(
            verification_type=VerificationType.ASSERTION,
            passed=len(issues) == 0,
            coverage=coverage,
            issues=issues,
            suggestions=suggestions
        )

    def verify_code_coverage(self) -> VerificationResult:
        """Verify code coverage of the design."""
        issues = []
        suggestions = []
        coverage = 0.0

        # Check statement coverage
        statements = len(re.findall(r';', self.verilog_content))
        covered_statements = len(re.findall(r'assert.*?;|if.*?;|else.*?;', self.testbench_content))
        if statements > 0:
            coverage = (covered_statements / statements) * 100.0

        if coverage < 80.0:
            issues.append(f"Low code coverage: {coverage:.1f}%")
            suggestions.append("Add test cases to improve code coverage")

        # Check branch coverage
        branches = len(re.findall(r'if|case', self.verilog_content))
        if branches > 0 and not re.search(r'default\s*:', self.verilog_content):
            issues.append("Missing default case in case statements")
            suggestions.append("Add default cases for complete branch coverage")

        return VerificationResult(
            verification_type=VerificationType.COVERAGE,
            passed=coverage >= 80.0,
            coverage=coverage,
            issues=issues,
            suggestions=suggestions
        )

    def verify_all(self) -> Dict[str, Any]:
        """Perform all verifications and return results."""
        results = {
            "formal": self.verify_formal_properties(),
            "functional": self.verify_functional_coverage(),
            "assertion": self.verify_assertions(),
            "coverage": self.verify_code_coverage()
        }

        return self.generate_verification_report(results)

    def generate_verification_report(self, results: Dict[str, VerificationResult]) -> Dict[str, Any]:
        """Generate a detailed verification report."""
        report = {
            "summary": {
                "total_issues": sum(len(r.issues) for r in results.values()),
                "total_suggestions": sum(len(r.suggestions) for r in results.values()),
                "average_coverage": sum(r.coverage for r in results.values()) / len(results),
                "all_passed": all(r.passed for r in results.values())
            },
            "verifications": {}
        }

        for ver_type, result in results.items():
            report["verifications"][ver_type] = {
                "passed": result.passed,
                "coverage": result.coverage,
                "issues": result.issues,
                "suggestions": result.suggestions
            }

        return report

    def generate_assertions(self) -> str:
        """Generate SystemVerilog assertions based on design analysis."""
        assertions = []
        
        # Generate basic assertions
        if re.search(r'input.*reset', self.verilog_content):
            assertions.append("""
            // Reset assertion
            property reset_assertion;
                @(posedge clk) reset |-> ##1 (state == IDLE);
            endproperty
            assert property(reset_assertion);
            """)

        # Generate pipeline assertions
        if re.search(r'always\s*@\s*\(posedge\s+clk\)', self.verilog_content):
            assertions.append("""
            // Pipeline validity assertion
            property pipeline_valid;
                @(posedge clk) disable iff (reset)
                $stable(valid) |-> ##1 $stable(data);
            endproperty
            assert property(pipeline_valid);
            """)

        return "\n".join(assertions)

    def generate_coverage_model(self) -> str:
        """Generate SystemVerilog coverage model based on design analysis."""
        coverage_model = []

        # Generate state coverage
        if re.search(r'state', self.verilog_content):
            coverage_model.append("""
            covergroup state_coverage;
                state_cp: coverpoint state {
                    bins states[] = {[0:$]};
                    bins transitions[] = ([0:$] => [0:$]);
                }
            endgroup
            """)

        # Generate data coverage
        if re.search(r'data', self.verilog_content):
            coverage_model.append("""
            covergroup data_coverage;
                data_cp: coverpoint data {
                    bins zero = {0};
                    bins small = {[1:10]};
                    bins large = {[11:$]};
                }
            endgroup
            """)

        return "\n".join(coverage_model)

def main():
    """Main entry point for the design verifier."""
    try:
        # Initialize verifier
        verifier = DesignVerifier(
            verilog_file="test_output/risc_processor.v",
            testbench_file="test_output/risc_processor_tb.sv"
        )

        # Perform verification
        verification_report = verifier.verify_all()

        # Save verification report
        report_file = Path("test_output/verification_report.json")
        report_file.write_text(json.dumps(verification_report, indent=2))
        logger.info(f"Verification report generated: {report_file}")

        # Generate and save assertions
        assertions = verifier.generate_assertions()
        assertions_file = Path("test_output/generated_assertions.sv")
        assertions_file.write_text(assertions)
        logger.info(f"Generated assertions saved to: {assertions_file}")

        # Generate and save coverage model
        coverage_model = verifier.generate_coverage_model()
        coverage_file = Path("test_output/generated_coverage.sv")
        coverage_file.write_text(coverage_model)
        logger.info(f"Generated coverage model saved to: {coverage_file}")

    except Exception as e:
        logger.error(f"Verification failed: {str(e)}")
        raise

if __name__ == "__main__":
    main() 