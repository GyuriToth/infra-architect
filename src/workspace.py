import os
import shutil
from typing import List

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

    def apply_to_target(self, target_path: str, project_name: str):
        """
        Synchronizes archived artifacts into the target project filesystem.
        """
        workspace = os.path.join(self.base_dir, project_name)
        if not os.path.exists(workspace):
            raise FileNotFoundError(f"No local artifacts found for {project_name}")
            
        for root, dirs, files in os.walk(workspace):
            rel_dir = os.path.relpath(root, workspace)
            dest_dir = os.path.join(target_path, rel_dir)
            os.makedirs(dest_dir, exist_ok=True)
            
            for file in files:
                shutil.copy2(os.path.join(root, file), os.path.join(dest_dir, file))
