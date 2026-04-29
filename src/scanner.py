import os
from typing import List, Dict, Set

class RepoScanner:
    """
    Performs deep scanning of the local repository to identify technology stacks.
    Supports monorepo detection and specific framework identification (Laravel, FastAPI, etc.).
    """
    def __init__(self, root_path: str):
        self.root_path = root_path
        self.ignore_dirs = {'.git', 'node_modules', '__pycache__', 'target', 'build', '.gradle', '.idea', 'venv', '.venv'}
        self.ignore_files = {'.DS_Store', 'Thumbs.db', 'package-lock.json', 'yarn.lock'}

    def scan(self) -> Dict:
        """
        Scans the repository structure and returns a tech stack analysis.
        """
        structure = []
        files_found: Set[str] = set()
        
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            rel_path = os.path.relpath(root, self.root_path)
            if rel_path == ".":
                rel_path = ""
            
            for file in files:
                if file not in self.ignore_files:
                    full_rel_path = os.path.join(rel_path, file)
                    structure.append(full_rel_path)
                    files_found.add(file)

        tech_stack = self._detect_tech_stack(files_found, structure)
        
        return {
            "root": self.root_path,
            "tech_stack": tech_stack,
            "file_count": len(structure),
            "files": structure[:100]
        }

    def _detect_tech_stack(self, file_names: Set[str], structure: List[str]) -> List[str]:
        """
        Internal heuristic logic to identify languages and frameworks.
        """
        detected: Set[str] = set()
        
        def has_file(name: str) -> bool:
            return name in file_names or any(name in f for f in structure)

        def has_ext(ext: str) -> bool:
            return any(f.endswith(ext) for f in structure)

        if has_file("pom.xml") or has_file("build.gradle"):
            detected.add("Java/Spring")
        
        if has_file("package.json"):
            detected.add("React/Node")
            
        if has_file("requirements.txt") or has_file("pyproject.toml") or has_ext(".py"):
            if has_file("manage.py"):
                detected.add("Python/Django")
            elif any("app" in f and f.endswith(".py") for f in structure):
                detected.add("Python/FastAPI-Flask")
            else:
                detected.add("Python")
                
        if has_file("go.mod") or has_ext(".go"):
            detected.add("Go")

        if has_file("composer.json") or has_ext(".php"):
            if has_file("artisan"):
                detected.add("PHP/Laravel")
            else:
                detected.add("PHP")

        # Monorepo detection logic
        manifests = [f for f in structure if os.path.basename(f) in {"package.json", "go.mod", "pom.xml", "requirements.txt", "composer.json"}]
        if len(manifests) > 1:
            dirs = {os.path.dirname(f) for f in manifests if os.path.dirname(f)}
            if len(dirs) > 1:
                detected.add("Monorepo")
            
        return sorted(list(detected))
