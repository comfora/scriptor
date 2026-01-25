"""
Scriptor is a open-source CLI tool designed for simple management of your local and cloud environments tailored to your home-labs or business environments
"""

import json
import requests
import os
import sys
from importlib.metadata import version
from loguru import logger

__VERSION__ = version("scriptor")

logger.remove()
logger.add(sys.stderr, level="ERROR")
logger.add("scriptor.log", rotation="50 MB", level="DEBUG")

CONFIG_JSON = {
    "sentry": {
        "disabled": False,
        "environment": "",
        "dsn": "https://22ce5a484332162e4855845e9a8a0a55@o4509176688082944.ingest.us.sentry.io/4510610903597056",
    }
}

DISCLAIMERS = {
    "": "[yellow]Warning:[/yellow] The developer, [DEVELOPER] has not provided any tags for this project.",
    "alpha": "[yellow]Caution:[/yellow] This project is marked as alpha. It may contain unstable or experimental features.",
    "beta": "[yellow]Caution:[/yellow] This project is marked as beta. It may contain unstable or experimental features.",
    "freemium": "[yellow]Info:[/yellow] This project follows a freemium model. Some features may require payment or subscription for full access.",
    "paid": "[yellow]Info:[/yellow] This project is a paid offering. Ensure you understand the pricing and licensing terms before use.",
    "enterprise": "[yellow]Info:[/yellow] This project is designed for enterprise use. It may include features or requirements specific to business environments.",
    "open-source": "[green]Good News:[/green] This project is open-source. You can review the source code and contribute to its development.",
}

PROJECT_JSON = {
    "name": "example-scriptor-project",
    "version": "0.1.0",
    "developer": "Example Developer",
    "description": "An example Scriptor project initialized using the CLI.",
    "endpoint": "main.py",
    "SCRIPTOR_API_VERSION": "v0",
}


class comforaConfig:
    def __init__(self):
        self.configPath = os.path.join(
            os.path.expanduser("~"), ".comfora", "scriptor", "config.json"
        )
        self._ensure_config_exists()
        self.configData = self.load_config()
        logger.debug(f"Configuration path set to: {self.configPath}")

    def _ensure_config_exists(self):
        """Create the config directory and file if they don't exist."""
        config_dir = os.path.dirname(self.configPath)

        # Create directory structure if it doesn't exist
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            logger.info(f"Created configuration directory: {config_dir}")

        # Create config file with empty JSON object if it doesn't exist
        if not os.path.exists(self.configPath):
            with open(self.configPath, "w") as f:
                json.dump(CONFIG_JSON, f, indent=4)
            logger.info(f"Created configuration file: {self.configPath}")

    def load_config(self):
        """Load configuration from file."""
        try:
            with open(self.configPath, "r") as f:
                config = json.load(f)
                logger.debug("Configuration file loaded successfully.")
                return config
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding configuration file: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error loading configuration file: {e}")
            return {}

    def manage_setting(self, setting: str, value=None):
        """
        Manages reading and writing settings to the configuration file.

        Args:
            setting: The setting key to read or write
            value: If provided, sets the setting to this value. If None, retrieves the setting.

        Returns:
            The setting value if value=None, otherwise None
        """
        try:
            with open(self.configPath, "r+") as f:
                try:
                    config = json.load(f)
                except json.JSONDecodeError as e:
                    logger.error(f"Error decoding configuration file: {e}")
                    config = {}

                if value is not None:
                    config[setting] = value
                    f.seek(0)
                    json.dump(config, f, indent=4)
                    f.truncate()
                    logger.debug(f"Setting '{setting}' updated to '{value}'.")
                    self.configData[setting] = value
                else:
                    logger.debug(
                        f"Retrieving setting '{setting}': {config.get(setting)}"
                    )
                    return (
                        config.get(setting).lower()
                        if isinstance(config.get(setting), str)
                        else config.get(setting)
                    )
        except Exception as e:
            logger.error(f"Error managing setting '{setting}': {e}")
            if value is None:
                return None


def validate_url(url: str):
    """
    Validates if a given URL is properly formatted and is reachable.
    """
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)

        # Consider the URL working if status code is in the 200–399 range
        return 200 <= response.status_code < 400

    except requests.exceptions.MissingSchema:
        print(f"Invalid URL format: {url}")
    except requests.exceptions.ConnectionError:
        print(f"Connection error: Unable to reach {url}")
    except requests.exceptions.Timeout:
        print(f"Timeout: {url} took too long to respond")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
