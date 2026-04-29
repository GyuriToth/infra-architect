import os
import anthropic
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class AIService:
    """
    Handles asynchronous communication with the Anthropic Claude API.
    Manages client initialization, prompt loading, and artifact generation.
    """
    def __init__(self, model: str = "claude-sonnet-4-6"):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self._client = None

    @property
    def client(self):
        """
        Lazily initializes the AsyncAnthropic client.
        """
        if not self._client:
            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
            self._client = anthropic.AsyncAnthropic(api_key=self.api_key)
        return self._client

    async def generate_artifact(self, system_prompt: str, user_content: str) -> str:
        """
        Sends an asynchronous request to Claude to generate a infrastructure artifact.
        
        Args:
            system_prompt: The persona and rules for the AI agent.
            user_content: The specific project context and generation request.
            
        Returns:
            The raw text content of the generated artifact.
        """
        try:
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_content}
                ]
            )
            return message.content[0].text
        except Exception as e:
            raise RuntimeError(f"AI Generation failed: {str(e)}")

    def load_prompt(self, prompt_name: str) -> str:
        """
        Loads a prompt template from the versioned prompts directory.
        Uses absolute path resolution to ensure compatibility with various launch contexts.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        prompt_path = os.path.join(project_root, "prompts", f"{prompt_name}.md")
        
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt file {prompt_path} not found")
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
