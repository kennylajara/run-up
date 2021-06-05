from os import walk
from typing import List


def get_version()->str:
    """Simple function to read RunUp's version"""
    with open('./version/runup.version') as f:
        return f.read()


def get_yaml_latest_version()->str:
    """Simple function to read RunUp's version"""
    with open('./version/yaml.version') as f:
        versions = f.read()
    versions.split(',')

    return versions[-1]


def list_yaml_versions()->List:
    """Simple function to read RunUp's version"""
    with open('./version/yaml.version') as f:
        versions = f.read()
    return versions.split(',')