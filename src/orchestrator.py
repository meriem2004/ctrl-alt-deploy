
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from validators.parser import parse_deployment_spec, ParseError
from infrastructure.generators.terraform_generator import generate_terraform_config
from infrastructure.executors.terraform_executor import TerraformExecutor


console = Console()

class DeploymentOrchestrator:
    def __init__(self):
        self.spec = None

    def run(self, spec_path: str):
        
        console.print(Panel.fit(f"[bold blue]🚀 Starting Deployment for: {spec_path}[/bold blue]"))

        # Step 1: Validation
        if not self.validate(spec_path):
            console.print("[bold red]⛔ Deployment Aborted due to validation errors.[/bold red]")
            return False

        # Step 2: Generate Terraform configuration
        terraform_dir = generate_terraform_config(self.spec)

        # Step 3: Execute Terraform
        executor = TerraformExecutor(terraform_dir)

        if not executor.init():
            return False

        if not executor.plan():
            return False

        if not executor.apply():
            return False

        console.print(Panel.fit("[bold green]✨ Deployment Sequence Completed![/bold green]"))
        return True

    def validate(self, spec_path: str) -> bool:
       
        console.print("\n[bold cyan]🔍 Step 1: Validating Specification...[/bold cyan]")
        try:
            self.spec = parse_deployment_spec(spec_path)
            console.print("[green]  Syntax & Semantic Validation Passed[/green]")
            return True
        except ParseError as e:
            console.print(f"[red]   Validation Failed: {e}[/red]")
            return False
        except Exception as e:
            console.print(f"[red]  Unexpected Error: {e}[/red]")
            return False

    def plan(self):
        """
        Generate Terraform plan (Stub).
        """
        console.print("\n[bold cyan]Step 2: Generating Execution Plan...[/bold cyan]")
        console.print("[yellow]    Terraform generation is not yet implemented.[/yellow]")
        console.print("[dim]  (This step would convert the parsed spec into .tf files)[/dim]")

    def apply(self):
        """
        Apply infrastructure changes (Stub).
        """
        console.print("\n[bold cyan]  Step 3: Provisioning Infrastructure...[/bold cyan]")
        console.print("[yellow]    Infrastructure provisioning is not yet implemented.[/yellow]")
        console.print("[dim]  (This step would run 'terraform apply')[/dim]")
