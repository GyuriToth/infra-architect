import os
import pytest
from src.scanner import RepoScanner

def test_scanner_detection():
    # Test on the current repository
    scanner = RepoScanner(os.getcwd())
    result = scanner.scan()
    
    assert "root" in result
    assert any("Python" in s for s in result["tech_stack"])
    assert result["file_count"] >= 5
    
    # Check for specific files in the scan
    files = result["files"]
    assert any(f.endswith("AI_STEERING.md") for f in files)
    assert any("src/server.py" in f or "server.py" in f for f in files)

def test_scanner_ignore_patterns(tmp_path):
    # Create a dummy repo with some ignored directories
    repo_dir = tmp_path / "dummy_repo"
    repo_dir.mkdir()
    (repo_dir / "node_modules").mkdir()
    (repo_dir / "node_modules" / "secret.txt").write_text("shhh")
    (repo_dir / ".git").mkdir()
    (repo_dir / ".git" / "config").write_text("config")
    (repo_dir / "src").mkdir()
    (repo_dir / "src" / "main.py").write_text("print('hello')")
    (repo_dir / "package.json").write_text("{}")
    
    scanner = RepoScanner(str(repo_dir))
    result = scanner.scan()
    
    assert "React/Node" in result["tech_stack"]
    assert any("Python" in s for s in result["tech_stack"])
    
    # node_modules and .git should be ignored
    files = result["files"]
    assert not any("node_modules" in f for f in files)
    assert not any(".git" in f for f in files)
    assert any("package.json" in f for f in files)
    assert any("src/main.py" in f or "main.py" in f for f in files)
