from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_upload_pdf():
    # Create a dummy file
    files = {"file": ("test.pdf", b"dummy pdf content", "application/pdf")}
    response = client.post("/api/generate-recap", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "markdown_summary" in data
    assert "image_url" in data
