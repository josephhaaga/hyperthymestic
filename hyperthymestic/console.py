import textwrap

import click
from configparser import ConfigParser

from hyperthymestic import __version__
from hyperthymestic.utils import config_file_path
from hyperthymestic.utils import get_config
from hyperthymestic.utils import write_config


@click.group()
@click.version_option(version=__version__)
def cli():
    """A search utility for your Markdown knowledge base."""
    pass


@cli.command()
def main() -> int:
    try:
        configuration = get_config()
        click.echo(textwrap.fill("This content is textwrapped because it goes " + ("on and " * 50)))
        return 0
    except FileNotFoundError:
        click.secho("Configuration not found. Run `hyperthymestic init` to generate a configuration.", fg="yellow")
        return 1


@cli.command()
def init() -> int:
    """Configure hyperthymestic to monitor your knowledge base."""
    configuration = get_config()
    kb_directory = click.prompt("Path to folder containing Markdown files", type=click.Path(exists=True)) #, confirmation_prompt=True)
    if 'hyperthymestic' not in configuration:
        configuration['hyperthymestic'] = {}
    configuration['hyperthymestic']['kb_directory_path'] = kb_directory
    write_config(configuration)
    return 0
    # set up config file and sqlite
    # also store sqlite.db in config folder

if __name__ == '__main__':
    cli()
