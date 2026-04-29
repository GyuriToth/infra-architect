import os
import shutil
import re
from typing import List, Dict

class WorkspaceManager:
    """
    Manages local artifact storage and project isolation.
    Ensures that generated files are archived before being applied to target repositories.
    """
    def __init__(self, base_dir: str = "ci-cd"):
        self.base_dir = base_dir
        if not os.path.isabs(self.base_dir):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            self.base_dir = os.path.join(project_root, base_dir)
        
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def get_project_workspace(self, target_path: str) -> str:
        """
        Creates a dedicated workspace directory for an external project.
        """
        project_name = os.path.basename(os.path.normpath(target_path))
        if not project_name:
            project_name = "unknown_project"
            
        workspace_path = os.path.join(self.base_dir, project_name)
        if not os.path.exists(workspace_path):
            os.makedirs(workspace_path)
            
        return workspace_path

    def save_artifact(self, target_path: str, filename: str, content: str):
        """
        Saves a generated configuration to the local archive.
        """
        workspace = self.get_project_workspace(target_path)
        file_path = os.path.join(workspace, filename)
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return file_path

    def extract_and_save_files(self, target_path: str, ai_content: str) -> List[str]:
        """
        Parses AI response for code blocks and saves them as individual files.
        Returns a list of saved file paths.
        """
        workspace = self.get_project_workspace(target_path)
        saved_files = []

        # Save the full response as a README first
        readme_path = self.save_artifact(target_path, "INFRA_LOG.md", ai_content)
        saved_files.append(readme_path)

        # Regex to find code blocks with optional language tags
        # Format: ```[language]\n[code]\n```
        pattern = r"```(?:\w+)?\n(.*?)\n```"
        blocks = re.findall(pattern, ai_content, re.DOTALL)

        for block in blocks:
            # Heuristic to determine filename based on content
            filename = None
            if "FROM " in block.upper() and "RUN " in block.upper():
                filename = "Dockerfile"
            elif "version:" in block and "services:" in block:
                filename = "docker-compose.yml"
            elif "on:" in block and "jobs:" in block:
                filename = ".github/workflows/main.yml"
            elif "trigger:" in block and "pool:" in block:
                filename = "azure-pipelines.yml"
            
            if filename:
                file_path = os.path.join(workspace, filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(block.strip())
                saved_files.append(file_path)

        return saved_files

    def apply_to_target(self, target_path: str, project_name: str):
        """
        Synchronizes archived artifacts into the target project filesystem.
        """
        workspace = os.path.join(self.base_dir, project_name)
        if not os.path.exists(workspace):
            raise FileNotFoundError(f"No local artifacts found for {project_name}")
            
        for root, dirs, files in os.walk(workspace):
            # Skip the log file during application
            files = [f for f in files if f != "INFRA_LOG.md"]
            
            rel_dir = os.path.relpath(root, workspace)
            dest_dir = os.path.join(target_path, rel_dir)
            os.makedirs(dest_dir, exist_ok=True)
            
            for file in files:
                shutil.copy2(os.path.join(root, file), os.path.join(dest_dir, file))
