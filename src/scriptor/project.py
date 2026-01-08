import typer
import json
from rich import print
from rich.panel import Panel
from scriptor import logger

app = typer.Typer(no_args_is_help=True)


@app.command(name="validate")
def validate():
    """
    Ensures the project metadata is valid and your project is executable by Scriptor.
    """

    # with open("scriptor.json", "r") as f:
    # localProject = json.load(f)
    # logger.debug("Loaded local scriptor.json file for validation.")


@app.command(name="showcase")
def showcase():
    """
    Gives you a visual representation on what end users will see downloading your project.
    """
    try:
        with open("scriptor.json", "r") as f:
            localProject = json.load(f)
    except FileNotFoundError:
        logger.error("No scriptor.json file found in the current directory.")
        raise typer.Exit(code=1)
    logger.debug("Loaded local scriptor.json file for showcase.")
    print(
        Panel.fit(
            f"[bold magenta]{localProject.get('name', 'Unknown')}[/bold magenta] - {localProject.get('version', 'N/A')}\n{localProject.get('description', 'No description available.')}\nDeveloped by, [green]{localProject.get('developer', 'Anonymous')}[/green]",
        )
    )

    logger.debug("Preparing additional disclaimers based on project tags.")
    additionalDisclaimers = []
    try:
        tags = localProject.get("tags", [])
    except Exception as e:
        logger.error(f"Error retrieving tags from scriptor.json: {e}")
        tags = []
    disclaimers = {
        "": "[yellow]Warning:[/yellow] This project is not marked with any tags. Consider adding tags to improve discoverability and functionality.",
        "alpha": "[yellow]Caution:[/yellow] This project is marked as alpha. It may contain unstable or experimental features.",
        "3rd-party": "[yellow]Note:[/yellow] This project contains services or features developed by third-party contributors. Ensure you trust the source before use.",
        "freemium": "[yellow]Info:[/yellow] This project follows a freemium model. Some features may require payment or subscription for full access.",
        "paid": "[yellow]Info:[/yellow] This project is a paid offering. Ensure you understand the pricing and licensing terms before use.",
        "enterprise": "[yellow]Info:[/yellow] This project is designed for enterprise use. It may include features or requirements specific to business environments.",
        "open-source": "[green]Good News:[/green] This project is open-source. You can review the source code and contribute to its development.",
    }

    for tag, message in disclaimers.items():
        if tag == "" and not tags:
            logger.warning("No tags found; adding general disclaimer.")
            additionalDisclaimers.append(message)
        elif tag in tags:
            logger.info(f"Tag '{tag}' found; adding corresponding disclaimer.")
            additionalDisclaimers.append(message)

    if additionalDisclaimers:
        print(
            Panel.fit(
                "\n".join(additionalDisclaimers),
                title="Additional Notes / Disclaimers",
                title_align="left",
            )
        )


if __name__ == "__main__":
    app()
