import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.server import mcp

def test_fastapi_root():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "AI-Infra Architect API is running"}

def test_fastapi_status():
    with TestClient(app) as client:
        response = client.get("/status")
        assert response.status_code == 200
        assert response.json()["status"] == "ready"
        assert response.json()["mcp_enabled"] is True

def test_mcp_foundation():
    # Verify MCP server is initialized and has tools
    assert mcp.name == "AI-Infra-Architect"
    # FastMCP stores tools in a specific way, let's just check if our tools are registered
    tool_names = [tool.name for tool in mcp._tool_manager.list_tools()]
    assert "scan_repository" in tool_names
    assert "generate_config" in tool_names
