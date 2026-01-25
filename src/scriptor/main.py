import json
import typer
import os
import scriptor.project as project
import sentry_sdk
from rich import print
from rich.panel import Panel
from typing_extensions import Annotated
from scriptor import __VERSION__, logger, comforaConfig, CONFIG_JSON

app = typer.Typer(no_args_is_help=True)
app.add_typer(
    project.app,
    name="project",
    help="Subset of Scriptor commands related to project management.",
)
config = comforaConfig()


@app.callback()
def callback(
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose", "-v", help="Enables verbose logging for debugging purposes."
        ),
    ] = False,
):
    """
    Scriptor is a open-source CLI tool designed for simple management of your local and cloud environments tailored to your home-labs or business environments
    """
    if verbose:
        # Until a better solution is found, we reconfigure the logger to show debug messages
        import sys

        logger.remove()
        logger.add(sys.stderr, level="DEBUG")
        logger.debug("Verbose logging enabled.")
        logger.add("scriptor.log", rotation="50 MB", level="DEBUG")

    sentry_config = comforaConfig().manage_setting("sentry")

    if sentry_config is None or sentry_config.get("disabled") is True:
        logger.info("Sentry error tracking is disabled in the configuration.")
        return
    else:
        if sentry_config.get("environment") == "dev":
            logger.debug("Sentry environment converted to `Dev`.")
            comforaEnvironment = "Dev"
        else:
            logger.debug("Sentry environment converted to `Public`.")
            comforaEnvironment = "Public"

        sentry_sdk.init(
            dsn=sentry_config.get("dsn"),
            environment=comforaEnvironment,
            traces_sample_rate=0.2,
            send_default_pii=False,
            release=__VERSION__,
        )
        logger.info("Sentry error tracking initialized.")

    logger.debug(f"Command invoked running {__VERSION__} version of Scriptor.")


@app.command(name="version")
def version():
    """
    Showcases information about scriptor including API and package versions.
    """
    print(Panel.fit(f"Installed Scriptor Version: [red]{__VERSION__}"))


@app.command(name="init")
def initialize(
    override: Annotated[
        bool,
        typer.Option(
            "--override", help="Override existing configuration file if it exists"
        ),
    ] = False,
):
    """
    Initializes a Scriptor project by setting up necessary configurations and directories.
    """
    logger.debug(
        f"Prepped API version {CONFIG_JSON['SCRIPTOR_API_VERSION']} for project initialization."
    )

    if os.path.exists("scriptor.json") and not override:
        logger.warning("Configuration already exists and --override not specified.")
        print(
            "Configuration file already exists, please add --override to recreate the file."
        )
        return
    with open("scriptor.json", "w") as file:
        logger.info("Creating scriptor.json configuration file.")
        file.write(json.dumps(CONFIG_JSON, indent=4))

    print(
        f"Scriptor v{CONFIG_JSON['SCRIPTOR_API_VERSION']} compatible project created.\n"
        "Note that Scriptor is still [yellow]under development[/yellow], some features may not work as expected and major changes are expected."
    )
    return


if __name__ == "__main__":
    app()
