# System Architecture: Course Recap Generator

This document outlines the system architecture and data flow for the Course Recap Generator application.

## Architecture Diagram

```mermaid
graph TD
    %% Define styles
    classDef frontend fill:#3b82f6,stroke:#2563eb,stroke-width:2px,color:white;
    classDef backend fill:#10b981,stroke:#059669,stroke-width:2px,color:white;
    classDef agent fill:#8b5cf6,stroke:#7c3aed,stroke-width:2px,color:white;
    classDef external fill:#f59e0b,stroke:#d97706,stroke-width:2px,color:white;

    %% Frontend Components
    subgraph Client ["Frontend (Vite + React)"]
        UI[Web UI - File Upload & Dashboard]:::frontend
    end

    %% Backend Components
    subgraph Server ["Backend (FastAPI)"]
        API[API Endpoint: /api/generate-recap]:::backend
        PDF[PDF Extraction Utility]:::backend
        
        %% Agent Workflow
        subgraph Workflow ["Agent Harness Workflow"]
            MainAgent[Main Agent: Summarizer]:::agent
            SubAgent[Sub-Agent: Reviewer]:::agent
        end
    end

    %% External Systems
    subgraph External ["External Services"]
        Canva[Canva MCP Server]:::external
    end

    %% Data Flow Connections
    UI -- "1. Uploads PDF/DOC" --> API
    API -- "2. Passes File" --> PDF
    PDF -- "3. Extracts Raw Text" --> MainAgent
    MainAgent -- "4. Generates Summary" --> SubAgent
    SubAgent -- "5. Verifies against Raw Text" --> MainAgent
    MainAgent -- "6. Sends Verified Summary" --> Canva
    Canva -- "7. Returns Diagram Image URL" --> MainAgent
    MainAgent -- "8. Returns Markdown + Image URL" --> API
    API -- "9. Sends JSON Response" --> UI
```

## Component Breakdown

1. **Client (Vite + React)**
   - Responsible for presenting a rich, glassmorphic UI to the user.
   - Handles file selection and displays the final generated output (Markdown text + Canva Image).

2. **Server (FastAPI)**
   - Acts as the bridge between the web interface and the local Agent workflow.
   - Handles file reception, temporary storage, and session logging for rollbacks.

3. **PDF Extraction Utility**
   - A lightweight Python script (using PyMuPDF or PyPDF2) that strips all raw text from the uploaded documents.

4. **Agent Harness Workflow**
   - **Main Agent:** Summarizes the raw text into a structured, topic-by-topic Markdown format.
   - **Sub-Agent:** Spawns to independently verify the generated summary against the original text, ensuring no missing concepts or hallucinations.

5. **External Services (Canva MCP)**
   - The Main Agent connects to the local Canva MCP server to automatically generate a visual diagram based on the verified summary.
