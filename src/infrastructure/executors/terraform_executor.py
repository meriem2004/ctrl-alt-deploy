import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()


class TerraformExecutor:
    def __init__(self, terraform_dir: str | Path):
        self.terraform_dir = Path(terraform_dir)
        self._step_header_printed = False  # ✅ NEW (minimal)

    def _run(self, command: list[str], title: str) -> bool:
        """
        Run a Terraform command and stream output directly to the terminal.
        """
        # Print step header ONCE before the first terraform command
        if not self._step_header_printed:
            console.print("\n[bold cyan]🔍 Step 3: Execute Terraform[/bold cyan]\n")
            self._step_header_printed = True

        console.print(Panel.fit(f"[bold cyan]{title}[/bold cyan]"))

        result = subprocess.run(
            command,
            cwd=self.terraform_dir,
            shell=False
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
