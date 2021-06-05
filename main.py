# Built-in
from interpreter import Interpreter
import click

# Own
from runup import Config, ParserYAML
from utils.runup import get_version


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

    yaml_parser = ParserYAML(config.context)
    interpreter:Interpreter = yaml_parser.parse()
    interpreter.set_environment(verbose=config.verbose)

    click.echo('Initiated')

if __name__ == "__main__":
    cli()
