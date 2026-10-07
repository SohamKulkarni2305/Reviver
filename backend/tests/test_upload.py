from fastapi.testclient import TestClient
from app import app

from unittest.mock import patch

client = TestClient(app)

@patch("workflow.extract_text")
def test_upload_pdf(mock_extract):
    mock_extract.return_value = "This is a test summary. " * 20
    # Create a dummy file
    files = {"file": ("test.pdf", b"dummy pdf content", "application/pdf")}
    response = client.post("/api/generate-recap", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "markdown_summary" in data
    assert "image_url" in data
