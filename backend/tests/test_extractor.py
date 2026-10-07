import pytest
from unittest.mock import patch, mock_open
from extractor import extract_text

@patch("extractor.PdfReader")
def test_extract_text(mock_pdf_reader):
    # Mock the behavior of PdfReader
    mock_pdf = mock_pdf_reader.return_value
    
    # Create a mock page object with extract_text method
    class MockPage:
        def extract_text(self):
            return "This is a test summary."
            
    mock_pdf.pages = [MockPage(), MockPage()]
    
    # Run the function
    result = extract_text("dummy.pdf")
    
    # Verify the result combines the text from both pages
    assert result == "This is a test summary.\nThis is a test summary."
