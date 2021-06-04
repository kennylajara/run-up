import click
from runup import Config, DotRunup


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('-c', '--context', type=click.Path(), default=Config.context)
@click.option('--verbose', is_flag=True,
              help='Show more information about the internal process.')
@click.version_option(package_name='runup', prog_name='RunUp')
@pass_config
def cli(config, context, verbose):
    """A simple backup system that only saves the files that has changed."""

    config.context = context
    config.verbose = verbose

    if verbose:
        click.echo('Verbose mode: ON')
        click.echo(f'verbose: {verbose}')
        click.echo(f'Context: {context}')


@cli.command()
@pass_config
def init(config):
    """Initialize the backup system."""

    print('Initiated')


if __name__ == "__main__":
    cli()