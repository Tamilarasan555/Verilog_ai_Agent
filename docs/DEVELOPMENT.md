# Development Guide

This guide provides detailed information for developers working on the MCP Verilog project.

## Development Environment

### Prerequisites

- Python 3.10 or later
- Git
- Verilog simulation tools (Icarus Verilog, ModelSim, etc.)
- OpenAI API key
- DeepSeek API key

### Setting Up the Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mcp_verilog.git
cd mcp_verilog
```

2. Run the development setup script:
```bash
./scripts/dev.sh
```

This script will:
- Create a virtual environment
- Install dependencies
- Set up the project structure
- Run code quality checks
- Run tests

### Project Structure

```
mcp_verilog/
├── src/
│   └── mcp_verilog/        # Main package
│       ├── agents/         # AI agents
│       │   └── verilog_ai_agent.py
│       ├── tools/          # Verilog tools
│       │   ├── verilog_generator.py
│       │   ├── design_optimizer.py
│       │   ├── design_verifier.py
│       │   ├── doc_generator.py
│       │   └── code_quality_analyzer.py
│       ├── utils/          # Utility functions
│       ├── mcp_server.py   # MCP server
│       └── mcp_client.py   # MCP client
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── fixtures/          # Test fixtures
└── docs/                  # Documentation
```

## Code Style

### Python Code Style

The project follows these style guidelines:
- PEP 8 for general Python style
- Black for code formatting
- isort for import sorting
- mypy for type checking
- ruff for linting

### Verilog Code Style

Verilog code should follow:
- IEEE 1364-2005 standard
- Consistent indentation (2 spaces)
- Clear module and port naming
- Comprehensive comments
- Proper parameter naming

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_verilog_generator.py

# Run tests with coverage
pytest --cov=src --cov-report=term-missing
```

### Writing Tests

1. Unit Tests:
   - Place in `tests/unit/`
   - Test individual components
   - Use pytest fixtures
   - Mock external dependencies

2. Integration Tests:
   - Place in `tests/integration/`
   - Test component interactions
   - Use real dependencies
   - Test end-to-end workflows

### Test Fixtures

Common test fixtures are available in `tests/fixtures/`:
- `verilog_code`: Sample Verilog code
- `testbench`: Sample testbench
- `design_spec`: Design specifications

## Adding New Features

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature
```

### 2. Implement the Feature

- Follow code style guidelines
- Add type hints
- Write docstrings
- Add tests
- Update documentation

### 3. Run Quality Checks

```bash
# Format code
black src tests
isort src tests

# Type checking
mypy src

# Linting
ruff check src tests

# Run tests
pytest
```

### 4. Commit Changes

```bash
git add .
git commit -m "Add your feature"
```

### 5. Push Changes

```bash
git push origin feature/your-feature
```

## Debugging

### Logging

The project uses Python's logging module:
```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Debug Mode

Enable debug mode by setting the environment variable:
```bash
export LOG_LEVEL=DEBUG
```

### Common Issues

1. MCP Connection Issues:
   - Check server is running
   - Verify port availability
   - Check firewall settings

2. Verilog Generation Issues:
   - Check API keys
   - Verify input format
   - Check log files

3. Test Failures:
   - Check test environment
   - Verify dependencies
   - Check log files

## Documentation

### Updating Documentation

1. Update README.md for user-facing changes
2. Update DEVELOPMENT.md for developer-facing changes
3. Add docstrings to new functions/classes
4. Update API documentation

### Generating Documentation

```bash
# Generate API documentation
pdoc --html src/mcp_verilog -o docs/api
```

## Release Process

1. Update version in pyproject.toml
2. Update CHANGELOG.md
3. Create release branch
4. Run tests and quality checks
5. Create release tag
6. Push to PyPI

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and quality checks
5. Submit a pull request

### Pull Request Guidelines

- Clear description of changes
- Link to related issues
- Update documentation
- Add tests for new features
- Follow code style guidelines

## Support

For support:
- Open an issue on GitHub
- Check the documentation
- Contact the maintainers 