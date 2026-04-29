import pytest
from src.validator import ArtifactValidator

def test_dockerfile_validation():
    validator = ArtifactValidator()
    
    valid_df = "FROM python:3.9-slim\nWORKDIR /app\nCOPY . .\nCMD ['python', 'app.py']"
    invalid_df = "WORKDIR /app\nCOPY . .\nCMD ['python', 'app.py']"
    
    is_valid, errors = validator.validate_dockerfile(valid_df)
    assert is_valid
    
    is_valid, errors = validator.validate_dockerfile(invalid_df)
    assert not is_valid
    assert "FROM" in errors[0]

def test_yaml_validation():
    validator = ArtifactValidator()
    
    valid_yaml = "version: '3.8'\nservices:\n  web:\n    build: ."
    invalid_yaml = "version: '3.8'\nservices:\n  web:\n    build: .  : extra"
    
    is_valid, errors = validator.validate_yaml(valid_yaml)
    assert is_valid
    
    is_valid, errors = validator.validate_yaml(invalid_yaml)
    assert not is_valid
    assert len(errors) > 0
