import os
import tomllib

def load_user_config() -> dict:
    path = os.path.join(os.getcwd(), ".filemerger.toml")
    if not os.path.isfile(path):
        return {}

    with open(path, "rb") as f:
        return tomllib.load(f)
