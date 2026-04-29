import os
import pytest
from src.scanner import RepoScanner

def test_scanner_php_detection(tmp_path):
    repo_dir = tmp_path / "php_repo"
    repo_dir.mkdir()
    (repo_dir / "index.php").write_text("<?php echo 'hello'; ?>")
    (repo_dir / "composer.json").write_text("{}")
    
    scanner = RepoScanner(str(repo_dir))
    result = scanner.scan()
    assert "PHP" in result["tech_stack"]

def test_scanner_laravel_detection(tmp_path):
    repo_dir = tmp_path / "laravel_repo"
    repo_dir.mkdir()
    (repo_dir / "artisan").write_text("#!/usr/bin/env php")
    (repo_dir / "composer.json").write_text("{}")
    
    scanner = RepoScanner(str(repo_dir))
    result = scanner.scan()
    assert "PHP/Laravel" in result["tech_stack"]

def test_scanner_monorepo_detection(tmp_path):
    repo_dir = tmp_path / "monorepo"
    repo_dir.mkdir()
    
    # Service A (Python)
    (repo_dir / "service_a").mkdir()
    (repo_dir / "service_a" / "requirements.txt").write_text("fastapi")
    
    # Service B (Node)
    (repo_dir / "service_b").mkdir()
    (repo_dir / "service_b" / "package.json").write_text("{}")
    
    scanner = RepoScanner(str(repo_dir))
    result = scanner.scan()
    assert "Monorepo" in result["tech_stack"]
    assert "Python" in result["tech_stack"]
    assert "React/Node" in result["tech_stack"]

def test_scanner_go_detection(tmp_path):
    repo_dir = tmp_path / "go_repo"
    repo_dir.mkdir()
    (repo_dir / "main.go").write_text("package main")
    
    scanner = RepoScanner(str(repo_dir))
    result = scanner.scan()
    assert "Go" in result["tech_stack"]
