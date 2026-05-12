import os
import yaml

def load_config(config_path: str = "config/config.yaml") -> dict:
    """
    Load the configuration from a YAML file.

    Args:
        config_path (str): The path to the configuration file.
    """
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config