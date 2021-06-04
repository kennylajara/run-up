from pathlib import Path
import sqlite3

import click
import yaml


class Config(object):
    """Default config of the "Global" args and kwargs."""

    context:str = '.'
    verbose:bool = False


class RunupDB:
    """
    Handle the database where the data is stored.
    
    The `.runup` files are CSV-formated files containing the
    path to the file, MD5 sign, SHA256 sign and ID of the backup
    where this file was found the first time.
    """
    
    def create(self, context:click.Path):
        """Create a new `runup.db`."""
        pass


class RunupYAML:
    """Analizer of the `runup.yml` or `runup.yaml` file."""

    def parse(self, context):
        """
        It parse the YAML file and sends the data to the interpreter.
        
        All YAML files need to have a `version`. The version in 
        the file decides which interpreter is going to be called. 
        This is to allow for improved system capabilities while 
        maintaining backwards compatibility.
        """
        pass

    def _read_yaml_file(self, context):
        """Automatically detect and read the `runup.yml` or `runup.yaml`."""
        
        yaml_file = Path(f"{context}/runup.yaml")
        yml_file = Path(f"{context}/runup.yml")
        if yaml_file.is_file():
            # file exists
            pass
        elif yml_file.is_file():
            # file exists
            pass
        else:
            raise FileNotFoundError(f'No runup.yaml file has been found in the given context: {context}')

