# Built-in
import sys
from typing import Dict, Optional, Union

# 3rd Party
import click

# Own
from runup.interpreter import Interpreter
from runup.version import runup_version
from runup.yaml_parser import ParserYAML
from runup.utils import vCall, vResponse


class Config(object):
    """Default config of the "Global" args and kwargs."""

    context:str = '.'
    interpreter:Optional[Interpreter] = None
    verbose:bool = False
    yaml:Optional[Dict[str, Union[str]]] = None

pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('-c', '--context', type=click.Path(), default=Config.context,
              help="Directory where the runup.yaml is located.")
@click.option('--verbose', is_flag=True,
              help='Show more information about the internal process.')
@click.version_option(version=runup_version, prog_name='RunUp')
@pass_config
def cli(config:Config, context:str, verbose:bool):
    """A simple backup system that only saves the files that has changed."""

    config.context = context
    config.verbose = verbose

    if verbose:
        click.echo('-'*10)
        click.echo(f'RunUp, version {runup_version}')
        click.echo('-'*10)
        click.echo(f'verbose: {verbose}')
        click.echo(f'Context: {context}')
        click.echo('-'*10)

    # Parse YAML file
    vCall(config.verbose, 'ParserYAML.parse')
    config.yaml, config.interpreter = ParserYAML(
        context=config.context, 
        verbose=config.verbose,
    ).parse()
    vResponse(config.verbose, 'ParserYAML.parse', config.interpreter)


@cli.command()
@pass_config
def init(config):
    """Initialize the backup system."""

    # Take actions
    if config.interpreter is not None:
        vCall(config.verbose, 'Interpreter:set_environment')
        env_set:bool = config.interpreter.set_environment()
        vResponse(config.verbose, 'Interpreter:set_environment', env_set)

        if env_set:
            click.echo('RunUp has been initialized successfully.')
    else:
        # click.echo('Interpreter not detected.')
        sys.exit(1)


@cli.command()
@click.argument('project', type=str, default='')
@click.option('--restore', is_flag=True,
            help="Change execution mode to restore backup.")
@pass_config
def backup(config, project:str, restore:bool):
    """Create a backup based on he yaml file config."""

    # Take actions
    if config.interpreter is not None:
        if restore:
            raise NotImplementedError('Restore Backup has not been implemented.')
            # vCall(config.verbose, 'Interpreter:restore_backup')
            # restored:bool = config.interpreter.restore_backup(config.yaml, project)
            # vResponse(config.verbose, 'Interpreter:restore_backup', restored)
            # if restored:
            #     click.echo('The backup has been restored.')
        else:
            vCall(config.verbose, 'Interpreter:create_backup')
            created:Optional[str] = config.interpreter.create_backup(config.yaml, project)
            vResponse(config.verbose, 'Interpreter:create_backup', created)
            if created is not None:
                click.echo('New backup created.')
    else:
        # click.echo('Interpreter not detected.')
        sys.exit(1)


if __name__ == "__main__":
    cli()
