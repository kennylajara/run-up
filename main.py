import click
from runup import Config, RunupDB, RunupYAML


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('-c', '--context', type=click.Path(), default=Config.context)
@click.option('--verbose', is_flag=True,
              help='Show more information about the internal process.')
@click.version_option(prog_name='RunUp') # package_name='runup', 
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

    parsed_yaml = RunupYAML()
    parsed_yaml.parse(config.context)
    print('Initiated')


if __name__ == "__main__":
    cli()
