# cython: language_level=3


# Built-in
import os
from pathlib import Path
from shutil import rmtree
import sys
from typing import Dict, Optional, Union, Any

# 3rd Party
import click
import pyximport  # type: ignore

pyximport.install()

# Own
from runup.config cimport Config
from runup.interpreter cimport Interpreter
from runup.utils cimport vCall, vResponse
from runup.version import RUNUP_VERSION
from runup.yaml_parser cimport ParserYAML


cpdef void set_config(config: Config, context: str, verbose: bint):
    """A simple backup system that only saves the files that has changed."""

    config.context = context
    config.verbose = verbose

    if verbose:
        click.echo("-" * 10)
        click.echo(f"RunUp, version {RUNUP_VERSION}")
        click.echo("-" * 10)
        click.echo(f"verbose: {verbose}")
        click.echo(f"Context: {context}")
        click.echo("-" * 10)

    # Parse YAML file
    vCall(config.verbose, "ParserYAML.parse")
    config.yaml, config.interpreter = ParserYAML(
        context=config.context,
        verbose=config.verbose,
    ).parse()
    vResponse(config.verbose, "ParserYAML.parse", config.interpreter)


cpdef bint init(config: Config):
    """Initialize the backup system."""

    # Take actions
    if config.interpreter is not None:
        vCall(config.verbose, "Interpreter:set_environment")
        env_set: bool = config.interpreter.set_environment()
        vResponse(config.verbose, "Interpreter:set_environment", env_set)

        if env_set:
            return True

    else:
        # click.echo('Interpreter not detected on Initialization.')
        sys.exit(1)


cpdef bint backup(config: Config, project: str):
    """Create a backup based on he yaml file config."""

    # Take actions
    if config.interpreter is not None:
        vCall(config.verbose, "Interpreter:create_backup")
        created: Optional[bool] = config.interpreter.create_backup(config.yaml, project)
        vResponse(config.verbose, "Interpreter:create_backup", created)
        if created is True:
            return True
        else:
            return False
    else:
        # click.echo('Interpreter not detected on backup creation.')
        sys.exit(1)

cpdef bint restore(
    config: Config, project: str, location: str, job: int, clear_location: bool, force: bool
):
    """Create a backup based on he yaml file config."""

    # Take actions
    if config.interpreter is not None:

        if clear_location:
            restored_backup_dir = str(f"{config.context}/{location}")
            for f in os.listdir(restored_backup_dir):
                if Path.is_dir(Path(f)):
                    if f == ".runup":
                        continue
                    rmtree(f)
                else:
                    if f == "runup.yaml":
                        continue
                    os.remove(os.path.join(restored_backup_dir, f))

        vCall(config.verbose, "Interpreter:restore_backup")
        restored: bool = config.interpreter.restore_backup(
            config.yaml, project, location, job, force
        )
        vResponse(config.verbose, "Interpreter:restore_backup", restored)
        if restored is None:
            return False
        else:
            return True
    else:
        # click.secho('Interpreter not detected on backup restore.', fg="red")
        sys.exit(0)