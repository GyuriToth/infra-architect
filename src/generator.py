import os
import json
from typing import Dict
from src.ai_service import AIService

class ConfigGenerator:
    """
    Orchestrates the creation of infrastructure and pipeline configurations.
    Uses specialized AI personas to generate optimized artifacts based on repo scans.
    """
    def __init__(self):
        self.ai_service = AIService()

    async def generate(self, scan_result: Dict) -> str:
        """
        Generates Docker and Docker Compose configurations.
        """
        tech_stack = ", ".join(scan_result.get("tech_stack", ["Unknown"]))
        file_structure = "\n".join(scan_result.get("files", []))

        system_prompt = self.ai_service.load_prompt("system_devops")
        docker_prompt_tmpl = self.ai_service.load_prompt("docker_gen")
        
        user_content = docker_prompt_tmpl.replace("{{tech_stack}}", tech_stack)
        user_content = user_content.replace("{{file_structure}}", file_structure)

        return await self.ai_service.generate_artifact(system_prompt, user_content)

    async def generate_workflow(self, scan_result: Dict) -> str:
        """
        Generates GitHub Actions CI/CD workflow configurations.
        """
        tech_stack = ", ".join(scan_result.get("tech_stack", ["Unknown"]))
        file_structure = "\n".join(scan_result.get("files", []))

        system_prompt = self.ai_service.load_prompt("system_devops")
        workflow_prompt_tmpl = self.ai_service.load_prompt("workflow_gen")
        
        user_content = workflow_prompt_tmpl.replace("{{tech_stack}}", tech_stack)
        user_content = user_content.replace("{{file_structure}}", file_structure)

        return await self.ai_service.generate_artifact(system_prompt, user_content)

    async def generate_azure_pipeline(self, scan_result: Dict) -> str:
        """
        Generates Azure DevOps YAML pipeline configurations.
        """
        tech_stack = ", ".join(scan_result.get("tech_stack", ["Unknown"]))
        file_structure = "\n".join(scan_result.get("files", []))

        system_prompt = self.ai_service.load_prompt("system_devops")
        azure_prompt_tmpl = self.ai_service.load_prompt("azure_devops_gen")
        
        user_content = azure_prompt_tmpl.replace("{{tech_stack}}", tech_stack)
        user_content = user_content.replace("{{file_structure}}", file_structure)

        return await self.ai_service.generate_artifact(system_prompt, user_content)
