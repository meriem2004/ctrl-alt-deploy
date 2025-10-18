"""
Main parser that orchestrates syntactic and semantic validation.
"""
import json
import yaml
from pathlib import Path
from typing import Union, Dict, Any
from pydantic import ValidationError as PydanticValidationError

from models.models import DeploymentSpec
from validators.semantic_validator import validate_spec_semantics


class ParseError(Exception):
    """Raised when parsing fails"""
    pass


class SpecParser:
    """
    Parses and validates deployment specification files.
    Handles both YAML and JSON formats.
    """
    
    def __init__(self, spec_file: Union[str, Path]):
        self.spec_file = Path(spec_file)
        self.raw_data: Dict[str, Any] = {}
        self.spec: DeploymentSpec | None = None
    
    def parse(self) -> DeploymentSpec:
        """
        Main parsing method - runs all validation steps.
        Returns validated DeploymentSpec object.
        Raises ParseError if validation fails.
        """
        print(f"📄 Parsing specification file: {self.spec_file}")
        
        # Step 1: Load file
        self.raw_data = self._load_file()
        print("✓ File loaded successfully")
        
        # Step 2: Syntactic validation (Pydantic)
        try:
            self.spec = DeploymentSpec(**self.raw_data)
            print("✓ Syntactic validation passed")
        except PydanticValidationError as e:
            self._handle_pydantic_errors(e)
        
        # Step 3: Semantic validation
        is_valid, errors, warnings = validate_spec_semantics(self.spec)
        
        # Display warnings
        if warnings:
            print("\n⚠️  Warnings:")
            for warning in warnings:
                print(f"  • {warning}")
        
        # Handle errors
        if errors:
            print("\n❌ Semantic validation failed:")
            for error in errors:
                print(f"  • {error}")
            raise ParseError(f"Semantic validation failed with {len(errors)} error(s)")
        
        print("✓ Semantic validation passed")
        print("\n✅ All validations passed! Specification is valid.\n")
        return self.spec
    
    def _load_file(self) -> Dict[str, Any]:
        """Load YAML or JSON file"""
        if not self.spec_file.exists():
            raise ParseError(f"Specification file not found: {self.spec_file}")
        
        try:
            with open(self.spec_file, 'r') as f:
                if self.spec_file.suffix in ['.yaml', '.yml']:
                    return yaml.safe_load(f)
                elif self.spec_file.suffix == '.json':
                    return json.load(f)
                else:
                    raise ParseError(
                        f"Unsupported file format: {self.spec_file.suffix}. "
                        f"Use .yaml, .yml, or .json"
                    )
        except yaml.YAMLError as e:
            raise ParseError(f"Invalid YAML syntax: {e}")
        except json.JSONDecodeError as e:
            raise ParseError(f"Invalid JSON syntax: {e}")
        except Exception as e:
            raise ParseError(f"Error reading file: {e}")
    
    def _handle_pydantic_errors(self, e: PydanticValidationError):
        """Format and display Pydantic validation errors"""
        print("\n❌ Syntactic validation failed:\n")
        
        for error in e.errors():
            location = " → ".join(str(loc) for loc in error['loc'])
            message = error['msg']
            error_type = error['type']
            
            print(f"  Location: {location}")
            print(f"  Error: {message}")
            print(f"  Type: {error_type}")
            print()
        
        raise ParseError(f"Syntactic validation failed with {len(e.errors())} error(s)")
    
    def get_summary(self) -> Dict[str, Any]:
        """Return a summary of the parsed specification"""
        if not self.spec:
            return {}
        
        return {
            "spec_version": self.spec.spec_version,
            "aws_region": self.spec.aws.region,
            "services_count": len(self.spec.application.services),
            "services": [
                {
                    "name": svc.name,
                    "type": svc.type,
                    "ports": svc.ports,
                    "has_scaling": svc.scaling is not None
                }
                for svc in self.spec.application.services
            ],
            "infrastructure": {
                "scalability": self.spec.infrastructure.scalability,
                "machine_size": self.spec.infrastructure.machine_size,
                "dns_enabled": self.spec.infrastructure.dns_enabled
            }
        }


def parse_deployment_spec(spec_file: Union[str, Path]) -> DeploymentSpec:
    """
    Convenience function to parse a deployment specification file.
    
    Args:
        spec_file: Path to YAML or JSON specification file
        
    Returns:
        Validated DeploymentSpec object
        
    Raises:
        ParseError: If validation fails
    """
    parser = SpecParser(spec_file)
    return parser.parse()