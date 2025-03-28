# Plan: Develop Core MCP Framework (Python SDK) & Verilog Code Agent Tool (v4 - Gemini Generation & Mandatory Linting)

**Overall Goal:** Create a foundational MCP server framework using the **official MCP Python SDK** and implement a primary `code_agent` tool that leverages the **Google Gemini model** to generate synthesizable Verilog/SystemVerilog RTL and basic testbenches based on detailed specifications, ensuring generated code passes basic linting.

**Assumptions:**

*   Development environment: Python (e.g., 3.10+), `uv` or `pip` for package management.
*   MCP SDK: `mcp-sdk-python`.
*   Schema validation: Pydantic.
*   Code Generation: **Google Gemini API** (via `google-generativeai` library).
*   **Google AI API Key:** Availability and secure management (e.g., via environment variables).
*   **Network Access:** Required for Gemini API calls.
*   Testing framework: `pytest`.
*   Linting Tool: An external Verilog linter (e.g., Verilator) accessible via command line.

---

## Phase 1: Core MCP Framework Development (Python SDK) (Estimate: 1 Week)

**Goal:** Establish a minimal, functional MCP server using the Python SDK, supporting basic tool registration and communication via STDIO and HTTP.

**Tasks:**

1.  **Project Setup & Structure** (Complexity: 2)
    *   Initialize Python project environment (e.g., `uv venv`, `uv pip install mcp-sdk-python pydantic pytest`).
    *   Define project directory structure (e.g., `src/server`, `src/tools`, `src/schemas`, `tests`).
    *   Configure project metadata (`pyproject.toml`).

2.  **Schema Definition (Pydantic)** (Complexity: 2)
    *   Define Pydantic models for basic MCP messages if needed (though the SDK should handle most).
    *   Define Pydantic models for a simple example tool's input/output.

3.  **Server Implementation (SDK)** (Complexity: 4)
    *   Utilize `mcp-sdk-python` components to create the main server application.
    *   Configure the server to use both STDIO and HTTP transports provided by the SDK.
    *   Implement the basic tool registration mechanism using the SDK's features.

4.  **Example Tool Implementation (SDK)** (Complexity: 3)
    *   Create a simple "echo" or "hello" tool class inheriting from the SDK's base tool class (e.g., `mcp_sdk.server.Tool`).
    *   Define its input/output using Pydantic models (Task 2).
    *   Implement the `execute` method.
    *   Register this tool with the server instance (Task 3).

5.  **Framework Integration & Validation** (Complexity: 3)
    *   Ensure the server starts correctly and registers the example tool.
    *   Write basic `pytest` tests for the example tool's execution logic.
    *   Manually test communication over both STDIO and HTTP using an MCP client or test utility compatible with the Python SDK.

**Phase 1 Deliverable:** A runnable MCP server built with the Python SDK, capable of hosting and executing a simple Pydantic-validated tool over STDIO and HTTP.

---

## Phase 2: `code_agent` Tool Development (Python with Gemini) (Estimate: 3-4 Weeks)

**Goal:** Implement the `code_agent` tool using the Gemini API for generation, ensuring generated RTL passes linting.

**Tasks:**

1.  **Define `code_agent` Schema (Pydantic)** (Complexity: 3)
    *   Define the detailed Pydantic model for the `code_agent` tool's input.
    *   Define the Pydantic model for the output: `verilog_code` (str), `testbench_code` (str), `success` (bool), `errors` (list[str], optional), `generation_info` (dict, optional - e.g., model used, warnings).

2.  **Setup Gemini API Integration** (Complexity: 3)
    *   Install `google-generativeai` library.
    *   Implement secure loading of the Google AI API key (e.g., from environment variables).
    *   Initialize the Gemini client (e.g., `genai.GenerativeModel('gemini-pro')` or a future equivalent specified like 'gemini-2.5').
    *   Implement basic API call wrapper with error handling (network errors, API errors, rate limits, content safety blocks).

3.  **Develop RTL Generation Logic (Gemini)** (Complexity: 8)
    *   Develop **prompt engineering strategy**: Create functions to translate the structured Pydantic input (ports, functionality, style, etc.) into a detailed, effective natural language prompt for Gemini requesting synthesizable Verilog RTL.
    *   Refine prompts iteratively based on Gemini output quality.
    *   Call the Gemini API via the wrapper (Task 2) with the generated prompt.
    *   Parse and extract the Verilog code block from the Gemini response. Handle cases where the response format might vary or code is incomplete.

4.  **Develop Basic Testbench Generation Logic (Gemini)** (Complexity: 7)
    *   Develop **prompt engineering strategy** for generating a basic SystemVerilog testbench based on the module definition (derived from input schema or potentially the generated RTL).
    *   Call the Gemini API via the wrapper (Task 2) with the testbench prompt.
    *   Parse and extract the SystemVerilog testbench code block from the Gemini response.

5.  **Implement `CodeAgentTool` Class (Python SDK)** (Complexity: 5)
    *   Create `src/tools/code_agent.py` implementing the SDK's `Tool` base class.
    *   Set `name`, `description`, link Pydantic schemas (Task 1).
    *   Implement the `execute` method:
        *   Call RTL generation logic (Task 3). Handle potential Gemini errors.
        *   Call Testbench generation logic (Task 4). Handle potential Gemini errors.
        *   Instantiate and return the Pydantic output model, including any errors or generation info.
    *   Register the `CodeAgentTool` with the server instance.

6.  **Testing the `code_agent` Tool (`pytest`)** (Complexity: 7)
    *   Write `pytest` unit tests for the prompt generation functions.
    *   Write integration tests for the `CodeAgentTool` using `pytest`:
        *   **Mock Gemini API calls** to test the tool's logic without actual API usage (essential for deterministic testing). Provide sample successful and error responses.
        *   Provide various valid input specifications.
        *   Execute the tool's `execute` method (using mocked API).
        *   Validate the *structure* and *syntax* of the parsed code from the mocked responses.
        *   **Mandatory:** Add a `pytest` fixture or test step that uses *pre-defined, known-good generated code samples* (or potentially code from a *real* Gemini call in specific, marked tests) saved to a temporary file and runs the external linter (e.g., `verilator --lint-only`) using `subprocess`. The test must fail if the linter reports errors.

7.  **Documentation** (Complexity: 3)
    *   Document the `code_agent` tool's Pydantic input/output schemas.
    *   Provide examples of input specifications.
    *   **Crucially:** Document the dependency on the Google AI API key and how to configure it.
    *   Update the main README with setup and usage instructions.

**Phase 2 Deliverable:** An MCP server (using Python SDK) hosting the `code_agent` tool, capable of calling the Google Gemini API to generate basic, lint-checked Verilog RTL and testbenches from Pydantic-validated inputs.

---

### Architecture Overview (Python SDK with Gemini & Linting)

```mermaid
graph TD
    subgraph "External Services"
        GeminiAPI[Google Gemini API]
    end

    subgraph "MCP Client"
        ClientApp[Client Application]
    end

    subgraph "MCP Server Framework (Python SDK - Phase 1)"
        SDKServer[MCP SDK Server (Handles Transport, Protocol)]
        SDKRegistry[SDK Tool Registration]
        SDKBaseTool[SDK Base Tool Class (Pydantic Integration)]
    end

    subgraph "Code Agent Tool (Python - Phase 2)"
        CodeAgent[CodeAgent Tool (Python)]
        PromptGenRTL[RTL Prompt Generation]
        PromptGenTB[TB Prompt Generation]
        GeminiWrapper[Gemini API Wrapper]
        ResponseParser[Response Parsing Logic]
    end

    subgraph "Testing (Phase 2)"
        Pytest[Pytest Integration Tests] --> CodeAgent
        Pytest -- Mocks --> GeminiWrapper
        Pytest -- Uses Sample Code --> TempFile[Temp Verilog File]
        Pytest -- Runs Linter --> Linter[External Linter (e.g., Verilator)]
        Linter -- Reads --> TempFile
        Linter -- Lint Results --> Pytest
    end

    ClientApp -- MCP Request (generate_rtl) --> SDKServer
    SDKServer -- Dispatches to Tool --> CodeAgent
    CodeAgent -- Inherits --> SDKBaseTool
    CodeAgent -- Validates Input (Pydantic) --> InputSchema[Input Pydantic Model]
    CodeAgent -- Uses --> PromptGenRTL
    CodeAgent -- Uses --> PromptGenTB
    PromptGenRTL -- Prompt --> GeminiWrapper
    PromptGenTB -- Prompt --> GeminiWrapper
    GeminiWrapper -- API Call --> GeminiAPI
    GeminiAPI -- Response --> GeminiWrapper
    GeminiWrapper -- Raw Response --> ResponseParser
    ResponseParser -- Parsed Code --> CodeAgent
    CodeAgent -- Returns Output (Pydantic) --> OutputSchema[Output Pydantic Model]
    SDKServer -- MCP Response --> ClientApp