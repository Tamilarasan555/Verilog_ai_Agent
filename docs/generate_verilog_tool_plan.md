# Plan: Create `generate_verilog_from_description` Tool

**Goal:** Create a new MCP tool within the `mcp_verilog_agent` server that generates Verilog code from a high-level functional description, automatically inferring the module interface (ports, parameters) using AI.

**Steps:**

1.  **Define Schemas:**
    *   Create new Pydantic models in `mcp_verilog_agent/schemas.py`:
        *   `GenerateFromDescriptionInput`: Contains `description: str` and optional `module_name_hint: Optional[str]`.
        *   `GenerateFromDescriptionOutput`: Contains `verilog_code: str` and optional `warnings: Optional[str]`.

2.  **Implement Tool Logic in `server.py`:**
    *   Create a new async function decorated with `@mcp.tool()`, named `generate_verilog_from_description`.
    *   **Step 1: Interface Inference (AI Call 1):**
        *   Use AI (e.g., DeepSeek Coder) to analyze the `description` and infer module name, ports (name, direction, width), and parameters (name, value) in a structured format (e.g., JSON).
        *   Parse the AI response, handling potential errors.
    *   **Step 2: Code Generation (AI Call 2):**
        *   Use AI (e.g., Gemini) to generate the complete Verilog module code (header and body) based on the original `description` and the inferred interface from Step 1.
    *   **Step 3: Return Output:**
        *   Package the generated code and any warnings (e.g., from inference uncertainty or generation issues) into the `GenerateFromDescriptionOutput` object.

3.  **Update Server:**
    *   Import new schemas in `server.py`.
    *   The `@mcp.tool()` decorator registers the new function.

**Flow Diagram:**

```mermaid
graph TD
    A[User provides High-Level Description] --> B(MCP Tool: generate_verilog_from_description);
    B -- Description --> C{Step 1: Infer Interface (AI)};
    C -- Inferred Interface --> D{Step 2: Generate Code (AI)};
    C -- Description --> D;
    D -- Generated Verilog Code --> E[Return Output (Code + Warnings)];
    C -- Inference Failure --> F[Handle Error / Return Warning];
    D -- Generation Failure --> F;
```

**Key Considerations:**

*   **AI Reliability:** Interface inference quality depends heavily on the AI's interpretation. Warnings for assumptions/low confidence are crucial.
*   **Error Handling:** Implement robust error handling for AI failures.
*   **Model Choice:** Leverage existing models (DeepSeek/Gemini) or explore alternatives.