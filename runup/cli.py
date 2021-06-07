# Built-in
from typing import List, Optional

# 3rd Party
import click

# Own
from runup.interpreter import Interpreter
from runup.version import runup_version
from runup.yaml_parser import ParserYAML



class Config(object):
    """Default config of the "Global" args and kwargs."""

    context:str = '.'
    debug:bool = False
    verbose:bool = False

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

@cli.command()
@pass_config
def init(config):
    """Initialize the backup system."""

    interpreter:Optional[Interpreter] = None

    # Parse YAML file
    interpreter = ParserYAML(
        context=config.context, 
        verbose=config.verbose,
    ).parse()

    # Take actions
    if interpreter is not None:
        if interpreter.set_environment():
            click.echo('New job initialized.')

if __name__ == "__main__":
    cli()
