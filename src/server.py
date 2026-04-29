from mcp.server.fastmcp import FastMCP
from src.scanner import RepoScanner
from src.workspace import WorkspaceManager
from src.generator import ConfigGenerator
import json
import os

# Initialize FastMCP server
mcp = FastMCP("AI-Infra-Architect")
generator = ConfigGenerator()
workspace_mgr = WorkspaceManager()

@mcp.tool()
async def scan_repository(path: str) -> str:
    """
    Scans the repository at the given path to identify project structure and tech stack.
    """
    try:
        scanner = RepoScanner(path)
        result = scanner.scan()
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error scanning repository: {str(e)}"

@mcp.tool()
async def generate_config(scan_result_json: str) -> str:
    """
    Generates Docker and Compose files, extracting them into real files locally.
    """
    try:
        scan_result = json.loads(scan_result_json)
        target_path = scan_result.get("root", "")
        
        result = await generator.generate(scan_result)
        
        if target_path:
            saved_paths = workspace_mgr.extract_and_save_files(target_path, result)
            paths_str = "\n".join([f"- {p}" for p in saved_paths])
            return f"FILES EXTRACTED AND SAVED TO:\n{paths_str}\n\n{result}"
            
        return result
    except Exception as e:
        return f"Error generating configuration: {str(e)}"

@mcp.tool()
async def generate_pipeline(scan_result_json: str) -> str:
    """
    Generates a GitHub Actions workflow and extracts it into a .yml file locally.
    """
    try:
        scan_result = json.loads(scan_result_json)
        target_path = scan_result.get("root", "")
        
        result = await generator.generate_workflow(scan_result)
        
        if target_path:
            saved_paths = workspace_mgr.extract_and_save_files(target_path, result)
            paths_str = "\n".join([f"- {p}" for p in saved_paths])
            return f"FILES EXTRACTED AND SAVED TO:\n{paths_str}\n\n{result}"
            
        return result
    except Exception as e:
        return f"Error generating pipeline: {str(e)}"

@mcp.tool()
async def generate_azure_pipeline(scan_result_json: str) -> str:
    """
    Generates an Azure DevOps pipeline and extracts it into a .yml file locally.
    """
    try:
        scan_result = json.loads(scan_result_json)
        target_path = scan_result.get("root", "")
        
        result = await generator.generate_azure_pipeline(scan_result)
        
        if target_path:
            saved_paths = workspace_mgr.extract_and_save_files(target_path, result)
            paths_str = "\n".join([f"- {p}" for p in saved_paths])
            return f"FILES EXTRACTED AND SAVED TO:\n{paths_str}\n\n{result}"
            
        return result
    except Exception as e:
        return f"Error generating Azure pipeline: {str(e)}"

@mcp.tool()
async def apply_artifacts(target_path: str) -> str:
    """
    Applies the generated artifacts from the local archive to the real project path.
    Only call this after you have generated the configs/pipelines.
    """
    try:
        project_name = os.path.basename(os.path.normpath(target_path))
        workspace_mgr.apply_to_target(target_path, project_name)
        return f"Successfully applied all artifacts to {target_path}"
    except Exception as e:
        return f"Error applying artifacts: {str(e)}"

if __name__ == "__main__":
    mcp.run()
