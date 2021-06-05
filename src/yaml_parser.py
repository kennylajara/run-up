# Built-in
from pathlib import Path
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

# 3rd Pary
import click
import yaml

# Own
from src.utils.version import (
    list_yaml_versions,
)
from src import interpreter


class ParserYAML:
    """Analizer of the `runup.yml` or `runup.yaml` file."""

    def __init__(self, context:str, verbose:bool):
        """Define the properties of the class."""
        self._context:str = context
        self._interpreter:Optional[interpreter.Interpreter] = None
        self._verbose:bool = verbose

    def parse(self)->Optional[Tuple[Path, interpreter.Interpreter]]:
        """
        It parse the YAML file and sends the data to the interpreter.
        
        All YAML files need to have a `version`. The version in 
        the file decides which interpreter is going to be called. 
        This is to allow for improved system capabilities while 
        maintaining backwards compatibility.
        """

        path:Path
        runup_config:Optional[Dict[str, Union[str]]]
        
        path, runup_config = self._read_yaml_file(context=self._context)
        
        if runup_config is None:
            return None

        version = self._get_version(runup_config)
        if version is None:
            return None

        if version == '1':
            my_interpreter = interpreter.Interpreter_1(path, verbose=self._verbose)
        else:
            return None

        return path, my_interpreter


    def _get_version(self, config)->Union[str,None]:
        """Get the version of the runup.yaml file."""
        
        if not 'version' in config:
            click.echo('The file `runup.yaml` should contain a version.')
            return None
        elif not isinstance(config['version'], str):
            click.echo(f"The version needs to be a string.")
            return None
        elif config['version'] not in list_yaml_versions():
            click.echo(f"The YAML version {config['version']} is not supported.")
            return None
        else:
            return config['version']


    def _read_yaml_file(self, context:str)->Tuple[Path,Optional[Dict[str, Union[str]]]]:
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
            click.echo(f'No `runup.yaml` file has been found in the given context: {context}')
            return yaml_path, None

        # Return YAML file
        with open(yaml_path, 'r') as stream:
            try:
                return yaml_path, yaml.safe_load(stream)
            except yaml.parser.ParserError as error:
                where = str(error.args[3]).strip()
                msg = f'Error {error.args[0]} {where}'
                click.echo(msg)
                return yaml_path, None
