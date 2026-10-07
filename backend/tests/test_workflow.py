import pytest
from unittest.mock import patch
from workflow import run_agent_workflow

@patch("workflow.extract_text")
@pytest.mark.anyio
async def test_workflow(mock_extract):
    # Setup mock
    mock_extract.return_value = "This is a test document. It contains important information about artificial intelligence. Artificial intelligence is a fascinating topic. We need to study artificial intelligence."
    
    # Run workflow
    result = await run_agent_workflow("dummy.pdf")
    
    # Verify outputs
    assert "markdown_summary" in result
    assert "artificial" in result["markdown_summary"].lower()
    assert "mermaid_code" in result
    assert "image_url" in result
