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
from runup import actions
from runup.config cimport Config
from runup.editor import Editor
from runup.interpreter cimport Interpreter
from runup.utils cimport vCall, vResponse
from runup.version import RUNUP_VERSION


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
def cli(config: Config, context: str, verbose: bint):
    """Common CLI actions."""

    # Take action
    actions.set_config(
        config=config,
        context=context,
        verbose=verbose
    )

@cli.command()
@pass_config
def init(config: Config):
    """Initialize the backup system."""

    # Take action
    result = actions.init(config)
    if result: 
        click.secho("RunUp has been initialized successfully.", fg="green")


@cli.command()
@click.argument("project", type=str, default="")
@pass_config
def backup(config: Config, project: str):
    """Create a backup based on he yaml file config."""

    # Take action
    result = actions.backup(
        config=config,
        project=project
    )
    if result is True:
        click.secho("New backup created.", fg="green")
    else:
        click.secho("The backup has NOT been created.", fg="red")


@cli.command()
@pass_config
def editor(config: Config):
    """Show the Graphic User Interfase (GUI)"""
    Editor()


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

    # Take action
    result = actions.restore(
        config=config, 
        project=project, 
        location=location, 
        job=job, 
        clear_location=clear_location, 
        force=force
    )
    if result is False:
        click.secho("The backup has NOT been restored.", fg="red")


if __name__ == "__main__":
    cli()
