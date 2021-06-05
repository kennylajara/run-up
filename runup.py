from pathlib import Path
import sqlite3
from typing import (
    Dict,
    List,
    Optional,
    Union,
)

import click
import yaml

from utils.runup import (
    get_version,
    list_yaml_versions,
)
import interpreter


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

    def __init__(self, context:str):
        """Define the properties of the class."""
        self._context:str = context
        self._interpreter:interpreter.Interpreter

    def parse(self)->None:
        """
        It parse the YAML file and sends the data to the interpreter.
        
        All YAML files need to have a `version`. The version in 
        the file decides which interpreter is going to be called. 
        This is to allow for improved system capabilities while 
        maintaining backwards compatibility.
        """

        runnup_config:Optional[Dict[str, Union[str]]] = self._read_yaml_file(context=self._context)
        if runnup_config is None:
            return None

        version = self._get_version(runnup_config)
        if version is None:
            return None

        if version == '1':
            self._interpreter = interpreter.Interpreter_1()


    def _get_version(self, config)->Union[str,None]:
        """Get the version of the runner.yaml file."""
        
        if not 'version' in config:
            click.echo('The file `runnup.yaml` should contain a version.')
            return None
        elif not isinstance(config['version'], str):
            click.echo(f"The version needs to be a string.")
            return None
        elif config['version'] not in list_yaml_versions():
            click.echo(f"The YAML version {config['version']} is not supported.")
            return None
        else:
            return config['version']


    def _read_yaml_file(self, context:str)->Optional[Dict[str, Union[str]]]:
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
            yaml_path:Path = Path(f"{context}{filename}")
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
                where = str(error.args[3]).strip()
                msg = f'Error {error.args[0]} {where}'
                click.echo(msg)
                return None
