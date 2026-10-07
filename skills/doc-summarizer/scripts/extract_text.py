"""
extract_text.py — Extract plain text from PDF, DOCX, or TXT files.

Usage:
    python extract_text.py "<absolute_file_path>"

Outputs extracted plain text to stdout.
Errors are printed to stderr with a non-zero exit code.
"""

import sys
import os


def extract(file_path: str) -> str:
    """Extract plain text from a PDF, DOCX, or TXT file.

    Args:
        file_path: Absolute or relative path to the document.

    Returns:
        Extracted plain text as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If file type is unsupported or no text could be extracted.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        text = open(file_path, encoding="utf-8").read()

    elif ext == ".pdf":
        try:
            import pdfplumber
        except ImportError:
            raise ImportError(
                "pdfplumber is required for PDF extraction. "
                "Run: pip install pdfplumber"
            )
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise ValueError(f"Could not read PDF file: {e}")

    elif ext == ".docx":
        try:
            from docx import Document
        except ImportError:
            raise ImportError(
                "python-docx is required for DOCX extraction. "
                "Run: pip install python-docx"
            )
        try:
            doc = Document(file_path)
            text = "\n".join(p.text for p in doc.paragraphs)
        except Exception as e:
            raise ValueError(f"Could not read DOCX file: {e}")

    else:
        raise ValueError(
            f"Unsupported file type: '{ext}'. Supported types: .pdf, .docx, .txt"
        )

    if not text.strip():
        raise ValueError(
            "No extractable text found in document. "
            "The file may be empty, image-only, or password-protected."
        )

    return text.strip()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python extract_text.py <file_path>",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        result = extract(sys.argv[1])
        print(result)
    except (FileNotFoundError, ValueError, ImportError) as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
