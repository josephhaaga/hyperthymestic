from datetime import datetime
from pathlib import Path
import textwrap

import click
from configparser import ConfigParser
import spacy

from hyperthymestic import __version__
from hyperthymestic.models import Document
from hyperthymestic.models import DocumentSnapshot
from hyperthymestic.utils import create_tables
from hyperthymestic.utils import get_config
from hyperthymestic.utils import get_database
from hyperthymestic.utils import hash_file
from hyperthymestic.utils import write_config


@click.group()
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx):
    """A search utility for your Markdown knowledge base."""
    ctx.ensure_object(dict)
    ctx.obj['config'] = get_config()
    _engine, ctx.obj['database'] = get_database()


@cli.command()
@click.pass_context
def main(ctx) -> int:
    db = ctx.obj['database']
    nlp = None #spacy.load("en_core_web_md")
    folder_path = Path(ctx.obj['config']['hyperthymestic']['kb_directory_path'])
    # USE TQDM AND SHOW HOW MANY DOCS ARE UPDATING
    for doc in sorted(list(folder_path.glob("*.md"))):
        is_new_doc = False
        hash_value = hash_file(doc)
        db_document = db.query(Document).filter_by(filepath=str(doc)).first()
        if db_document == None:
            click.secho(f"New document \"{doc.name}\"", fg="blue")
            d = Document(
                filename=doc.name,
                filepath=str(doc)
            )
            db.add(d)
            db.commit()
            db_document = d
            is_new_doc = True
        db_snapshot = db.query(DocumentSnapshot).filter_by(
            doc_id=db_document.id,
            hash=hash_value
        ).first()
        if db_snapshot == None:
            if not is_new_doc:
                click.secho(f"Updated document \"{doc.name}\"", fg="yellow")
            db_snapshot = DocumentSnapshot(
                doc_id=db_document.id,
                hash=hash_value,
                date_parsed=datetime.now()
            )
            db.add(db_snapshot)
            db.commit()
            if not nlp:
                nlp = spacy.load("en_core_web_md")
            parsed_doc = nlp(
            # DO NLP HERE AND COMMIT THE EMBEDDINGS
            # TODO create a custom spacy pipeline that will remove escape sequences, line escapes, etc.
        else:
            click.echo(f"Unchanged document \"{doc.name}\"")
    return 0


@cli.command()
@click.pass_context
def init(ctx) -> int:
    """Configure hyperthymestic to monitor your knowledge base."""
    configuration = ctx.obj['config']

    kb_directory = click.prompt(
        "Path to folder containing Markdown files",
        type=click.Path(exists=True)
    )
    if 'hyperthymestic' not in configuration:
        configuration['hyperthymestic'] = {}
    configuration['hyperthymestic']['kb_directory_path'] = kb_directory

    write_config(configuration)
    create_tables()
    return 0

#   example_doc = Document(filename="example.md", filepath="path/to/example.md")
#   session = ctx.obj['DATABASE']
#   session.add(example_doc)
#   session.commit()
#   q = session.query(Document)
#   print(q.first())


if __name__ == '__main__':
    cli(obj={})
