import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from models.models import DeploymentSpec
from infrastructure.generators.terraform_generator import generate_terraform_config

def main():
    spec_file = Path("test_app_spec.json")
    if not spec_file.exists():
        print(f"Error: {spec_file} not found")
        return

    try:
        # Load JSON
        with open(spec_file, "r") as f:
            data = json.load(f)
        
        # Parse and validate with Pydantic
        spec = DeploymentSpec(**data)
        
        # Generate Terraform
        output_dir = generate_terraform_config(spec, output_dir="terraform_test_output")
        
        print(f"Success! Terraform generated in {output_dir}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
