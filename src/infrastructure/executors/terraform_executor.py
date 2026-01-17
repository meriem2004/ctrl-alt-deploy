import subprocess
from pathlib import Path
from rich.console import Console

console = Console()


class TerraformExecutor:
    """
    Responsible for executing Terraform commands
    (init, plan, apply, destroy) on a generated Terraform directory.
    """

    def __init__(self, terraform_dir: Path):
        self.terraform_dir = terraform_dir

        if not self.terraform_dir.exists():
            raise ValueError(f"Terraform directory does not exist: {terraform_dir}")

    def init(self) -> bool:
        return self._run_command(["terraform", "init"])

    def plan(self) -> bool:
        return self._run_command(["terraform", "plan"])

    def apply(self, auto_approve: bool = True) -> bool:
        cmd = ["terraform", "apply"]
        if auto_approve:
            cmd.append("-auto-approve")
        return self._run_command(cmd)

    def destroy(self, auto_approve: bool = True) -> bool:
        cmd = ["terraform", "destroy"]
        if auto_approve:
            cmd.append("-auto-approve")
        return self._run_command(cmd)

    def _run_command(self, command: list[str]) -> bool:
        console.print(f"\n[bold cyan]▶ Running:[/bold cyan] {' '.join(command)}")

        process = subprocess.run(
            command,
            cwd=self.terraform_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if process.stdout:
            console.print(process.stdout)

        if process.returncode != 0:
            console.print(f"[bold red]Terraform command failed[/bold red]")
            console.print(process.stderr)
            return False

        return True
