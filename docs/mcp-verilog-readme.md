# MCP Verilog Server

## Overview
The MCP (Master Control Program) Verilog Server is a tool designed to assist in Verilog code generation and simulation based on natural language prompts. It leverages Icarus Verilog for simulation and provides a flexible interface for generating Verilog modules.

## Prerequisites
- Python 3.7+
- Icarus Verilog (iverilog)
- vvp (Icarus Verilog simulation runtime)

## Installation

1. Install Icarus Verilog:
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install iverilog

   # On macOS (using Homebrew)
   brew install icarus-verilog

   # On Windows
   # Download and install from http://iverilog.icarus.com/
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/your-username/mcp-verilog-server.git
   cd mcp-verilog-server
   ```

3. Set up a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

## Usage

### Basic Usage
```python
from mcp_verilog_server import MCPVerilogServer

# Create an MCP Server instance
mcp_server = MCPVerilogServer()

# Process a prompt
result = mcp_server.process_prompt("Create a simple counter")

# Access generation and simulation results
print(result['generation']['code'])  # Verilog code
print(result['simulation']['status'])  # Simulation status
```

### Command-Line Interface
```bash
python mcp_verilog_server.py
```

## Features
- Automatic Verilog code generation from prompts
- Built-in simulation using Icarus Verilog
- Support for various module types (counter, gates, flip-flops)
- Flexible prompt-based code generation

## Supported Prompts
- "Create a simple counter"
- "Design an AND gate"
- "Implement a D Flip-Flop"
- Custom module descriptions

## Limitations
- Code generation is currently based on predefined templates
- Sophisticated natural language processing not fully implemented
- Requires manual review and potential modifications of generated code

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
[Specify your license here, e.g., MIT, Apache 2.0]

## Disclaimer
This is a prototype tool and should be used with caution. Always review and validate generated Verilog code before use in production environments.
