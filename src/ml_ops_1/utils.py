import sys

import yaml


def load_yaml(path_to_config: str) -> dict:
    with open(path_to_config, "r") as f:
        config = yaml.safe_load(f)
    return config
