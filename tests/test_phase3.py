import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from src.ai_service import AIService
from src.generator import ConfigGenerator

@pytest.fixture
def mock_anthropic_client():
    with patch('anthropic.AsyncAnthropic') as mock:
        yield mock

@pytest.mark.asyncio
async def test_ai_service_generate(mock_anthropic_client):
    # Setup mock response
    mock_instance = mock_anthropic_client.return_value
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="MOCKED_CONFIG")]
    
    # Use AsyncMock for the awaitable call
    mock_instance.messages.create = AsyncMock(return_value=mock_message)
    
    # We need to set the environment variable for the test to pass the check
    with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'fake_key'}):
        ai_service = AIService()
        result = await ai_service.generate_artifact("system", "user")
        
        assert result == "MOCKED_CONFIG"
        mock_instance.messages.create.assert_called_once()

@pytest.mark.asyncio
async def test_generator_logic(mock_anthropic_client):
    mock_instance = mock_anthropic_client.return_value
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="DOCKER_CONFIG_YAML")]
    
    # Use AsyncMock for the awaitable call
    mock_instance.messages.create = AsyncMock(return_value=mock_message)
    
    with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'fake_key'}):
        generator = ConfigGenerator()
        scan_result = {
            "tech_stack": ["Python"],
            "files": ["main.py", "requirements.txt"]
        }
        
        result = await generator.generate(scan_result)
        assert result == "DOCKER_CONFIG_YAML"
        
        # Verify that prompts were loaded and substituted (indirectly by checking call)
        args, kwargs = mock_instance.messages.create.call_args
        assert "Python" in kwargs["messages"][0]["content"]
        assert "main.py" in kwargs["messages"][0]["content"]
