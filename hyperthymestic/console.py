import textwrap

import click

from . import __version__


@click.command()
@click.version_option(version=__version__)
def main():
    """A search utility for your Markdown knowledge base."""
    # look for xonfig file, or set one up (config file lists target directory)
    # also store sqlite.db in config folder
    # https://pypi.org/project/appdirs/
    # https://stackoverflow.com/a/7567946
    click.secho("Hello, world!", fg="green")
    click.echo(textwrap.fill("This content is textwrapped because it goes " + ("on and " * 50)))
