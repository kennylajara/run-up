# Built-in
from abc import ABC, abstractmethod
import os
from pathlib import Path

# 3rd party
import click

# Own
from runup.runupdb import RunupDB


class Interpreter(ABC):
    """Interpreters' abstract class."""

    @abstractmethod
    def __init__(self, context:Path, verbose:bool, version:str) -> None:
        """Set interpreter variables."""
        self._context:Path = context
        self._verbose:bool = verbose
        self._version:str = version
        
    @abstractmethod
    def create_backup(self) -> bool:
        """Create a new backup."""
        pass
        
    @abstractmethod
    def restore_backup(self, backup_id:str) -> bool:
        """Restore the specified backup."""
        pass

    @abstractmethod
    def set_environment(self) -> bool:
        """Create the backup enviroment."""
        pass


class Interpreter_1(Interpreter):
    """Interpreter that implements the rules for YAML version 1."""
    
    def __init__(self, context:Path, verbose:bool):
        super(Interpreter_1, self).__init__(
            context=context,
            verbose=verbose,
            version='1',
        )

    def create_backup(self) -> bool:
        pass

    def restore_backup(self, backup_id:str) -> bool:
        pass

    def set_environment(self) -> bool:
        """
        Create the backup enviroment.

        Creates a directory `.runup` at context level. In it
        creates a `.version` that only contains a number `1`
        and creates a SQLite database named `runup.db`.
        """

        if self._verbose:
            click.echo('Setting environment.')

        # Create the directory `.runup`
        if not os.path.exists(f'{self._context}/.runup'):
            os.mkdir(f'{self._context}/.runup')
            if self._verbose:
                click.echo(f'Created directory {self._context}/.runup')
        else:
            if self._verbose:
                click.echo(f'The directory `{self._context}/.runup` already exists.')
            click.echo('RunUp is already initiated.')
            return False
        
        # Create file `.version`
        if not os.path.exists(f'{self._context}/.runup/.version'):
            with open(f'{self._context}/.runup/.version', "w") as file:
                file.write(self._version)
            if self._verbose:
                click.echo(f'created file {self._context}/.runup/.version')
        else:
            if self._verbose:
                click.echo(f'The file `{self._context}/.runup/.version` already exists.')
            click.echo('RunUp is already initiated.')
            return False

        # Create database
        RunupDB(self._context, self._verbose).create_database()

        if self._verbose:
            click.echo('-'*10)

        return True
