import typer
app = typer.Typer()

#! Add more commands.
@app.callback()
def callback():
    """
    Scriptor is a open-source CLI tool designed for simple management of your local and cloud environments tailored to your home-labs or business environments
    """

# TODO: Need to add more information and dynamic versioning + commands.
@app.command()
def version():
    """
    Showcases information about scriptor including API and package versions.
    """
    print("Scriptor version 0.0.1")