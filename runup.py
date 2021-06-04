import click
import sqlite3
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
    """Intepreter of the `runup.yml` or `runup.yaml` file."""

    def parse(self, context):
        """
        It parse the YAML file and sends the data to the interpreter.
        
        All YAML files need to have a `version`. The version in 
        the file decides which interpreter is going to be called. 
        This is to allow for improved system capabilities while 
        maintaining backwards compatibility.
        """
        pass
