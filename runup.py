from pathlib import Path
import sqlite3
from typing import (
    List,
    Optional,
)

import click
import yaml


class Config(object):
    """Default config of the "Global" args and kwargs."""

    context:str = '.'
    debug:bool = False
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

    def parse(self, context:str, debug:bool) -> None:
        """
        It parse the YAML file and sends the data to the interpreter.
        
        All YAML files need to have a `version`. The version in 
        the file decides which interpreter is going to be called. 
        This is to allow for improved system capabilities while 
        maintaining backwards compatibility.
        """

        yaml_path:Optional[Path] = self._read_yaml_file(context=context, debug=debug)
        if yaml_path is None:
            return None

    def _read_yaml_file(self, context:str, debug:bool=False)->Optional[Path]:
        """Automatically detect a `runup.yml` or `runup.yaml` in the given context."""

        # Ensure context ends with /
        if not context.endswith('/'):
            context = f'{context}/'

        # Valid names for the YAML files
        supported_names:List[str] = [
            'runup.yaml', 'runup.yml'
        ]
        # Look for the files in the given context
        file_found:bool = False
        for filename in supported_names:
            yaml_path:Path = Path(f"{context}/{filename}")
            if yaml_path.is_file():
                file_found = True
                break
        
        # Raise error if the file has not been found.
        if not file_found:
            click.echo(f'No runup.yaml file has been found in the given context: {context}')
            return None

        # Return YAML file
        with open(yaml_path, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.parser.ParserError as error:
                msg = f'Error {error.args[0]}{error.args[3]}'
                click.echo(msg)
                return None
