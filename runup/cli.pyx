# cython: language_level=3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


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


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option(
    "-c",
    "--context",
    type=click.Path(),
    default=Config().context,
    help="Directory where the runup.yaml is located.",
)
@click.option(
    "--verbose", is_flag=True, help="Show more information about the internal process."
)
@click.version_option(version=RUNUP_VERSION, prog_name="RunUp")
@pass_config
def cli(Config config: Dict[str, Any], context: str, verbose: bint):
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

@cli.command()
@pass_config
def init(Config config):
    """Initialize the backup system."""

    # Take actions
    if config.interpreter is not None:
        vCall(config.verbose, "Interpreter:set_environment")
        env_set: bool = config.interpreter.set_environment()
        vResponse(config.verbose, "Interpreter:set_environment", env_set)

        if env_set:
            click.secho("RunUp has been initialized successfully.", fg="green")

    else:
        # click.echo('Interpreter not detected on Initialization.')
        sys.exit(1)


@cli.command()
@click.argument("project", type=str, default="")
@pass_config
def backup(Config config, project: str):
    """Create a backup based on he yaml file config."""

    # Take actions
    if config.interpreter is not None:
        vCall(config.verbose, "Interpreter:create_backup")
        created: Optional[bool] = config.interpreter.create_backup(config.yaml, project)
        vResponse(config.verbose, "Interpreter:create_backup", created)
        if created is True:
            click.secho("New backup created.", fg="green")
        else:
            click.secho("The backup has NOT been created.", fg="red")
    else:
        # click.echo('Interpreter not detected on backup creation.')
        sys.exit(1)


@cli.command()
@click.argument("project", type=str, default="")
@click.option(
    "-j",
    "--job",
    type=int,
    default=0,
    help="In restoration mode, indicates the number of the job "
    + "to be restored. Zero (default) to restore the latest "
    + "job.",
)
@click.option(
    "-l",
    "--location",
    type=str,
    default="",
    help="In restoration mode, indicates the location where "
    + "the backup should to be restored.",
)
@click.option(
    "--clear-location", is_flag=True, help="Empty location before restoration."
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Make the restore without asking a confirmation.",
)
@pass_config
def restore(
    Config config, project: str, location: str, job: int, clear_location: bool, force: bool
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
            click.secho("The backup has NOT been restored.", fg="red")
    else:
        # click.secho('Interpreter not detected on backup restore.', fg="red")
        sys.exit(0)


if __name__ == "__main__":
    cli()
