import sys

import yaml


def load_yaml(path_to_config: str) -> dict:
    with open(path_to_config, "r") as f:
        config = yaml.safe_load(f)
    return config

def pickle_load(path: str):
    if path[:-4]!='.pkl':
        path+='.pkl'
    with open(path, 'rb') as f:
        d=pickle.load(f)
    return d

def pickle_dump(data, path: str):
    if path[:-4]!='.pkl':
        path+='.pkl'
    with open(path, 'wb') as f:
        pickle.dump(data, f)