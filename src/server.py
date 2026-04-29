from mcp.server.fastmcp import FastMCP
from src.scanner import RepoScanner
import json

from src.generator import ConfigGenerator

# Initialize FastMCP server
mcp = FastMCP("AI-Infra-Architect")
generator = ConfigGenerator()

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
    Generates Docker and CI/CD configurations for a project based on its scan result.
    """
    try:
        scan_result = json.loads(scan_result_json)
        result = await generator.generate(scan_result)
        return result
    except Exception as e:
        return f"Error generating configuration: {str(e)}"

@mcp.tool()
async def generate_pipeline(scan_result_json: str) -> str:
    """
    Generates a GitHub Actions workflow pipeline based on project scan result.
    """
    try:
        scan_result = json.loads(scan_result_json)
        result = await generator.generate_workflow(scan_result)
        return result
    except Exception as e:
        return f"Error generating pipeline: {str(e)}"

@mcp.tool()
async def generate_azure_pipeline(scan_result_json: str) -> str:
    """
    Generates an Azure DevOps pipeline based on project scan result.
    """
    try:
        scan_result = json.loads(scan_result_json)
        result = await generator.generate_azure_pipeline(scan_result)
        return result
    except Exception as e:
        return f"Error generating Azure pipeline: {str(e)}"

if __name__ == "__main__":
    mcp.run()
