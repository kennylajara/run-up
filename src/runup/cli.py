# Built-in
from typing import Optional

# 3rd Party
import click

# Own
from src.runup.interpreter import Interpreter
from src.utils.version import get_version
from src.runup.yaml_parser import ParserYAML



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
@click.version_option(version=get_version(), prog_name='RunUp')
@pass_config
def cli(config:Config, context:str, verbose:bool):
    """A simple backup system that only saves the files that has changed."""

    config.context = context
    config.verbose = verbose

    if verbose:
        click.echo(f'verbose: {verbose}')
        click.echo(f'Context: {context}')
        click.echo('-'*10)

@cli.command()
@pass_config
def init(config):
    """Initialize the backup system."""

    yaml_parser = ParserYAML(config.context, verbose=config.verbose)
    interpreter:Optional[Interpreter] = yaml_parser.parse()
    if interpreter is not None:
        interpreter.set_environment(verbose=config.verbose)

if __name__ == "__main__":
    cli()
