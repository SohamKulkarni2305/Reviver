"""
test_integration.py — End-to-end integration test for extract_text.py
Verifies the full extraction pipeline works correctly on the sample fixture.
"""

import subprocess
import sys
import os

SCRIPT = os.path.join(os.path.dirname(__file__), "extract_text.py")
SAMPLE = os.path.join(os.path.dirname(__file__), "sample_doc.txt")


def test_txt_end_to_end():
    """Full pipeline: TXT file → extract_text.py → stdout with expected content."""
    result = subprocess.run(
        [sys.executable, SCRIPT, SAMPLE],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Script failed with stderr: {result.stderr}"
    assert "Machine learning" in result.stdout
    assert "Arthur Samuel" in result.stdout
    assert "supervised learning" in result.stdout
    assert "reinforcement learning" in result.stdout
    assert len(result.stdout.strip()) > 100, "Output is suspiciously short"


def test_path_with_quoted_spaces(tmp_path):
    """Paths with spaces are handled correctly on Windows."""
    folder = tmp_path / "my documents"
    folder.mkdir()
    f = folder / "notes.txt"
    f.write_text("This is a test document with spaces in the path.")
    result = subprocess.run(
        [sys.executable, SCRIPT, str(f)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    assert "test document with spaces" in result.stdout
