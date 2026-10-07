from PyPDF2 import PdfReader

def extract_text(file_path: str) -> str:
    """Extracts all text from a given PDF file."""
    try:
        reader = PdfReader(file_path)
        text_parts = []
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text_parts.append(extracted)
        return "\n".join(text_parts)
    except Exception as e:
        # In a real app we'd log this properly
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")
