import textwrap

import click
from configparser import ConfigParser

from hyperthymestic import __version__
from hyperthymestic.models import Document
from hyperthymestic.utils import create_tables
from hyperthymestic.utils import get_config
from hyperthymestic.utils import write_config
from hyperthymestic.utils import get_database


@click.group()
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx):
    """A search utility for your Markdown knowledge base."""
    ctx.ensure_object(dict)
    _engine, ctx.obj['database'] = get_database()

@cli.command()
@click.pass_context
def main(ctx) -> int:
    try:
        configuration = get_config()
        click.echo(textwrap.fill("This content is textwrapped because it goes " + ("on and " * 50)))
        return 0
    except FileNotFoundError:
        click.secho("Configuration not found. Run `hyperthymestic init` to generate a configuration.", fg="yellow")
        return 1


@cli.command()
@click.pass_context
def init(ctx) -> int:
    """Configure hyperthymestic to monitor your knowledge base."""
    configuration = get_config()

    kb_directory = click.prompt(
        "Path to folder containing Markdown files",
        type=click.Path(exists=True)
    )
    if 'hyperthymestic' not in configuration:
        configuration['hyperthymestic'] = {}
    configuration['hyperthymestic']['kb_directory_path'] = kb_directory

    write_config(configuration)

    create_tables()
    example_doc = Document(filename="example.md", filepath="path/to/example.md")
    session = ctx.obj['DATABASE']
    session.add(example_doc)
    session.commit()
    q = session.query(Document)
    print(q.first())

    return 0

if __name__ == '__main__':
    cli(obj={})
