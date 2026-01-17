import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()


class TerraformExecutor:
    def __init__(self, terraform_dir: str | Path):
        self.terraform_dir = Path(terraform_dir)

    def _run(self, command: list[str], title: str) -> bool:
        """
        Run a Terraform command and stream output directly to the terminal.
        """
        console.print(Panel.fit(f"[bold cyan]{title}[/bold cyan]"))

        result = subprocess.run(
            command,
            cwd=self.terraform_dir,
            shell=False
            # ❌ NO stdout=PIPE
            # ❌ NO stderr=PIPE
            # ✅ Terraform writes directly to PowerShell
        )

        if result.returncode != 0:
            console.print(
                f"[bold red]✗ Command failed:[/bold red] {' '.join(command)}"
            )
            return False

        console.print(f"[bold green]✓ {title} completed successfully[/bold green]")
        return True

    def init(self) -> bool:
        return self._run(
            ["terraform", "init"],
            "⚙️ Terraform Initialization"
        )

    def plan(self) -> bool:
        return self._run(
            ["terraform", "plan"],
            "📐 Terraform Plan"
        )

    def apply(self) -> bool:
        return self._run(
            ["terraform", "apply", "-auto-approve"],
            "🚀 Terraform Apply"
        )
