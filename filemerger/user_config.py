import os
import tomllib
from typing import Dict, Any

def load_user_config() -> Dict[str, Any]:
    """
    Load .filemerger.toml from the current working directory.
    Returns empty dict if not found.
    """
    config_path = os.path.join(os.getcwd(), ".filemerger.toml")
    if not os.path.isfile(config_path):
        return {}

    with open(config_path, "rb") as f:
        return tomllib.load(f)
