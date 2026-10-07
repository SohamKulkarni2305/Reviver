import pytest
from unittest.mock import patch
from backend.workflow import run_agent_workflow

@patch("backend.workflow.extract_text")
def test_workflow(mock_extract):
    # Setup mock
    mock_extract.return_value = "Course on AI Agents. Section 1: Intro. Section 2: MCP."
    
    # Run workflow
    result = run_agent_workflow("dummy.pdf")
    
    # Verify outputs
    assert "markdown_summary" in result
    assert "image_url" in result
    
    # Verify the workflow correctly structured the output
    assert "Section 1" in result["markdown_summary"]
    assert "canva.com" in result["image_url"]
