import typer
import sys
from pathlib import Path
from rich.console import Console
from orchestrator import DeploymentOrchestrator

# Add current directory to path to ensure imports work if run directly
sys.path.insert(0, str(Path(__file__).parent))

app = typer.Typer(help="🚀 Deployment Automation CLI")
console = Console()

@app.command()
def run(
    spec_file: str = typer.Argument(..., help="Path to the deployment specification file (JSON/YAML)")
):
    """
    Run the full deployment pipeline from a spec file.
    """
    orchestrator = DeploymentOrchestrator()
    success = orchestrator.run(spec_file)
    
    if not success:
        raise typer.Exit(code=1)

@app.command()
def validate(
    spec_file: str = typer.Argument(..., help="Path to the deployment specification file")
):
    """
    Only validate the specification without deploying.
    """
    orchestrator = DeploymentOrchestrator()
    success = orchestrator.validate(spec_file)
    
    if not success:
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
