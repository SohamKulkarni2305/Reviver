import subprocess
import sys
import os

SCRIPT = os.path.join(os.path.dirname(__file__), "extract_text.py")


def run(path):
    result = subprocess.run(
        [sys.executable, SCRIPT, path],
        capture_output=True,
        text=True,
    )
    return result


def test_txt_extraction(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("Hello world from TXT.")
    r = run(str(f))
    assert r.returncode == 0
    assert "Hello world from TXT." in r.stdout


def test_missing_file():
    r = run("nonexistent_file.pdf")
    assert r.returncode != 0
    assert "not found" in r.stderr.lower()


def test_unsupported_extension(tmp_path):
    f = tmp_path / "file.csv"
    f.write_text("a,b,c")
    r = run(str(f))
    assert r.returncode != 0
    assert "unsupported" in r.stderr.lower()


def test_empty_txt(tmp_path):
    f = tmp_path / "empty.txt"
    f.write_text("")
    r = run(str(f))
    assert r.returncode != 0
    assert "no extractable text" in r.stderr.lower()
