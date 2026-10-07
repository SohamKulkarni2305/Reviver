# Course Recap Generator Design Spec

## Overview
A web application and agentic workflow that takes PDF/DOC course slides as input and produces a verified, topic-structured summary along with a visual diagram. The project utilizes the Antigravity agent harness, custom skills, sub-agents, and the Canva MCP server to fulfill the Day 6 Assignment requirements.

## Architecture & Components

### 1. Frontend Web Application (Vite)
- **Tech Stack:** Vite, Vanilla HTML/JS, Vanilla CSS.
- **Aesthetics:** Modern, premium design featuring glassmorphism, dark mode, smooth gradients, and micro-animations.
- **Functionality:** 
  - Drag-and-drop file upload interface.
  - Loading state with micro-animations while the agent processes the file.
  - Results dashboard that displays the Markdown-formatted topic summary and embeds the Canva-generated visual diagram.

### 2. The Agent Harness Workflow
The core processing is handled by an Antigravity Custom Skill that orchestrates the following flow:
- **PDF Extraction:** A lightweight Python script extracts raw text from the uploaded PDF/DOC files.
- **Main Agent (Summarizer):** Processes the raw text and generates a structured summary, grouped logically by topic for readability.
- **Harness-Defined Sub-Agent (Reviewer):** A dedicated sub-agent spawned by the main harness. Its explicit role is to review the generated summary against the original extracted text to ensure accuracy and verify that no key concepts were missed.
- **Canva MCP Server:** The main agent passes the verified summary concepts to the Canva MCP server to generate an automated visual diagram (e.g., a mind map or concept flow).

## Data Flow
1. User uploads PDF via Web App.
2. Web App passes the file to the local Agent Workflow.
3. Text is extracted from PDF.
4. Main Agent summarizes text.
5. Sub-Agent reviews and verifies summary against the original text.
6. Main Agent calls Canva MCP to generate graphic.
7. Final output (Markdown summary + Image URL) is returned to the Web App and displayed.

## Constraints & Requirements Handled
- **Single Pass:** The agent loop is bounded and clean (Input -> Extract -> Summarize -> Review -> Visual -> Output) with no indefinite loops.
- **MCP Server:** Utilizes Canva MCP for diagram generation.
- **Sub-Agent:** Utilizes a dedicated review sub-agent.
- **Custom Skill:** The entire recap workflow is packaged as a reusable Antigravity skill (`course-recap-generator`).
- **Session Logging:** Maintains detailed session logs of all operations and intermediate states to ensure it is easy to roll back in case of errors.
