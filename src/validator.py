import subprocess
import yaml
import os
from typing import Tuple, List

class ArtifactValidator:
    """
    Validates generated artifacts against syntax rules and security best practices.
    Provides fail-fast feedback for the AI generation loop.
    """
    def validate_dockerfile(self, content: str) -> Tuple[bool, List[str]]:
        """
        Validates Dockerfile for multi-stage builds and non-root user enforcement.
        """
        errors = []
        warnings = []
        
        if "FROM" not in content.upper():
            errors.append("Dockerfile missing FROM instruction")
        
        from_count = content.upper().count("FROM")
        if from_count < 2:
            warnings.append("Recommendation: Use multi-stage builds to reduce image size.")
            
        if "USER" not in content.upper():
            warnings.append("Security Warning: Dockerfile does not specify a non-root USER.")

        return len(errors) == 0, errors + warnings

    def validate_yaml(self, content: str, artifact_type: str = "general") -> Tuple[bool, List[str]]:
        """
        Validates YAML syntax and basic schema requirements for workflows and compose files.
        """
        errors = []
        try:
            data = yaml.safe_load(content)
            
            if artifact_type == "workflow":
                if not isinstance(data, dict):
                    errors.append("Workflow must be a dictionary")
                elif "on" not in data or "jobs" not in data:
                    errors.append("Workflow missing mandatory 'on' or 'jobs' keys")
                    
            elif artifact_type == "compose":
                if not isinstance(data, dict):
                    errors.append("Docker-compose must be a dictionary")
                elif "services" not in data:
                    errors.append("Docker-compose missing 'services' key")
                    
        except yaml.YAMLError as exc:
            errors.append(f"YAML Syntax Error: {str(exc)}")
        
        return len(errors) == 0, errors

    def check_docker_compose_config(self, file_path: str) -> Tuple[bool, str]:
        """
        Uses system CLI tools (docker-compose) to validate configuration if available.
        Falls back to internal YAML validation if CLI tools are missing.
        """
        try:
            result = subprocess.run(
                ["docker-compose", "-f", file_path, "config"],
                capture_output=True, text=True, check=False
            )
            if result.returncode != 0:
                return False, result.stderr
            return True, "Valid"
        except FileNotFoundError:
            try:
                with open(file_path, "r") as f:
                    is_valid, errors = self.validate_yaml(f.read(), "compose")
                    return is_valid, "; ".join(errors) if errors else "Valid (YAML only)"
            except Exception as e:
                return False, f"Error reading file: {str(e)}"
