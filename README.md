# MCP Verilog

A Model Control Protocol (MCP) server with Verilog AI Agent integration for automated Verilog code generation, optimization, verification, and documentation.

## Features

- **Verilog Code Generation**: Generate Verilog code from natural language descriptions
- **Design Optimization**: Optimize Verilog designs for area, power, and timing
- **Design Verification**: Verify designs with testbenches and assertions
- **Documentation Generation**: Generate comprehensive documentation
- **MCP Integration**: Seamless integration with Model Control Protocol
- **RESTful API**: HTTP endpoints for all operations
- **Development Tools**: Code formatting, type checking, and linting

## Requirements

- Python 3.10 or later
- Verilog simulation tools (e.g., Icarus Verilog, ModelSim)
- OpenAI API key (for code generation)
- DeepSeek API key (for advanced analysis)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mcp_verilog.git
cd mcp_verilog
```

2. Set up the development environment:
```bash
# Make the development script executable
chmod +x scripts/dev.sh

# Run the development setup
./scripts/dev.sh
```

3. Create a `.env` file:
```bash
cp .env.example .env
```
Edit the `.env` file with your API keys and configuration.

## Project Structure

```
mcp_verilog/
├── src/
│   └── mcp_verilog/
│       ├── agents/          # AI agents
│       ├── tools/           # Verilog tools
│       ├── utils/           # Utility functions
│       ├── mcp_server.py    # MCP server
│       └── mcp_client.py    # MCP client
├── tests/                   # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── fixtures/           # Test fixtures
├── docs/                   # Documentation
├── logs/                   # Log files
├── mcp_output/            # Generated files
├── scripts/               # Development scripts
└── pyproject.toml         # Project configuration
```

## Usage

### Starting the Server

```bash
python scripts/dev_server.py
```

### Using the MCP Client

```python
from mcp_verilog import generate_verilog_design, optimize_design, verify_design

# Generate a design
result = await generate_verilog_design(
    description="Design a 4-bit counter",
    module_name="counter"
)

# Optimize a design
opt_result = await optimize_design(verilog_code)

# Verify a design
verify_result = await verify_design(verilog_code, testbench)
```

### Using the HTTP API

```bash
# Generate a design
curl -X POST http://localhost:8000/design/generate \
  -H "Content-Type: application/json" \
  -d '{"description": "Design a 4-bit counter", "module_name": "counter"}'

# Get a design
curl http://localhost:8000/design/counter

# Optimize a design
curl -X POST http://localhost:8000/design/optimize \
  -H "Content-Type: application/json" \
  -d '{"verilog_code": "module counter..."}'

# Verify a design
curl -X POST http://localhost:8000/design/verify \
  -H "Content-Type: application/json" \
  -d '{"verilog_code": "module counter...", "testbench": "module counter_tb..."}'
```

## Development

### Code Style

The project uses:
- Black for code formatting
- isort for import sorting
- mypy for type checking
- ruff for linting

Run code quality checks:
```bash
# Format code
black src tests
isort src tests

# Type checking
mypy src

# Linting
ruff check src tests
```

### Testing

Run tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src --cov-report=term-missing
```

### Adding New Features

1. Create a new branch:
```bash
git checkout -b feature/your-feature
```

2. Make your changes

3. Run tests and code quality checks:
```bash
./scripts/dev.sh
```

4. Commit your changes:
```bash
git add .
git commit -m "Add your feature"
```

5. Push to your branch:
```bash
git push origin feature/your-feature
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and code quality checks
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Mission Control Protocol (MCP) team
- OpenAI for GPT models
- DeepSeek for advanced analysis capabilities
- The Verilog community for tools and resources 
# Verilog_ai_Agent
