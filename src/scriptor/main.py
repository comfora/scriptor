import sys
from importlib.metadata import PackageNotFoundError, metadata

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()


@app.callback()
def callback():
    """
    Scriptor is a open-source CLI tool designed for simple management of your local and cloud environments tailored to your home-labs or business environments
    """


@app.command()
def version():
    """
    Showcases information about scriptor including API and package versions.
    """
    try:
        pkg_metadata = metadata("scriptor")
    except PackageNotFoundError:
        console.print(
            "[red]Error: scriptor package not found. Please ensure it is installed.[/red]"
        )
        raise typer.Exit(code=1)

    table = Table(title="Scriptor Information", show_header=False)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Package", pkg_metadata["Name"])
    table.add_row("Version", pkg_metadata["Version"])
    table.add_row("Description", pkg_metadata["Summary"])
    table.add_row(
        "Python",
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    )

    console.print(table)
