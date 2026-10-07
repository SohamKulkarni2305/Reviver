# Course Recap Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Vite web app and Python-backed agent workflow that summarizes PDF/DOC course slides, verifies the summary with a sub-agent, generates a Canva visual, and returns a detailed markdown document.

**Architecture:** A Vite React frontend provides a modern, glassmorphic UI for file uploads. A Python backend handles the upload and triggers the Antigravity agent workflow using the Antigravity Python SDK (or local script equivalent). The workflow extracts text, summarizes, reviews via a sub-agent, uses the Canva MCP for visuals, logs the session, and returns the result to the frontend.

**Tech Stack:** React (Vite), Vanilla CSS, Python (FastAPI), PyMuPDF (or PyPDF2), Antigravity Agent Harness, Canva MCP.

**Spec:** `docs/superpowers/specs/2026-10-07-course-recap-generator-design.md`

## Global Constraints

- **Single Pass:** The agent loop is bounded and clean with no indefinite loops.
- **Session Logging:** Maintains detailed session logs of all operations and intermediate states for easy rollback.

## Review Focus

- **Empty or unreadable PDF files:** The PDF parser should gracefully fail and return a clear error message. (Tested in backend upload task).
- **Canva MCP failure:** If the Canva generation fails, the application should still return the text summary with a warning about the missing visual. (Tested in agent workflow task).
- **Sub-agent rejection:** If the sub-agent finds the summary lacking, it should automatically trigger a single retry or append its corrections. (Tested in agent workflow task).

---

### Task 1: Initialize Project Structure & Backend API

**Files:**
- Create: `backend/app.py`
- Create: `backend/requirements.txt`
- Test: `backend/tests/test_upload.py`

**Interfaces:**
- Produces: `POST /api/generate-recap` (accepts multipart/form-data file, returns JSON with `markdown_summary` and `image_url`)

- [ ] **Step 1: Write the failing test for the upload endpoint**

```python
def test_upload_pdf():
    # Mock file upload to /api/generate-recap
    # Assert response contains expected keys
    pass
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest backend/tests/test_upload.py`
Expected: FAIL

- [ ] **Step 3: Implement FastApi app in `backend/app.py`**
Create the FastAPI application with a `POST /api/generate-recap` endpoint that accepts a file, saves it temporarily, and for now returns a dummy response `{"markdown_summary": "# Summary", "image_url": ""}`. Include setup of `logging` to file `session.log` for rollback maintenance.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest backend/tests/test_upload.py`
Expected: PASS

- [ ] **Step 5: Commit**

### Task 2: PDF Extraction Utility

**Files:**
- Create: `backend/extractor.py`
- Test: `backend/tests/test_extractor.py`

**Interfaces:**
- Produces: `def extract_text(file_path: str) -> str:`

- [ ] **Step 1: Write the failing test**

```python
def test_extract_text():
    # Pass path to sample PDF, assert output string is not empty
    pass
```

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Implement `extract_text` using PyMuPDF or PyPDF2**

- [ ] **Step 4: Run test to verify it passes**

- [ ] **Step 5: Commit**

### Task 3: Agent Workflow Implementation (Main Agent, Sub-Agent, Canva)

**Files:**
- Create: `backend/workflow.py`
- Modify: `backend/app.py` (call workflow)
- Test: `backend/tests/test_workflow.py`

**Interfaces:**
- Consumes: `extract_text`
- Produces: `def run_agent_workflow(file_path: str) -> dict:`

- [ ] **Step 1: Write the failing test for workflow**

```python
def test_workflow():
    # Mock agent calls and Canva MCP call
    # Assert run_agent_workflow returns proper dict
    pass
```

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Implement `run_agent_workflow` in `backend/workflow.py`**
Implement the logic:
1. Log start of session.
2. Call `extract_text`.
3. Use a system prompt to summarize the text via an LLM call.
4. Spawn a sub-agent (or second LLM call explicitly acting as review sub-agent) to verify the summary against the original text.
5. Use the Canva MCP integration to generate an image based on the summary.
6. Log completion and return the markdown and image URL.

- [ ] **Step 4: Run test to verify it passes**

- [ ] **Step 5: Commit**

### Task 4: Vite React Frontend

**Files:**
- Create: `frontend/` (Vite app)
- Create: `frontend/src/App.jsx`
- Create: `frontend/src/index.css`

**Interfaces:**
- Consumes: `POST /api/generate-recap`

- [ ] **Step 1: Initialize Vite React app**
Run `npm create vite@latest frontend -- --template react`

- [ ] **Step 2: Implement `index.css` with modern aesthetics**
Add CSS for glassmorphism, dark mode, smooth gradients, and micro-animations.

- [ ] **Step 3: Implement `App.jsx`**
Create a drag-and-drop file upload zone. Create a loading state (spinner/animation) for when the API is called. Render the returned Markdown and Canva image URL in a clean dashboard.

- [ ] **Step 4: Test frontend manually via `npm run dev`**
Verify the UI looks premium and handles file upload -> loading -> display correctly.

- [ ] **Step 5: Commit**
