import click
from flask import Blueprint
from flask.cli import with_appcontext
from .seed import seed

blueprint = Blueprint('commands', __name__, cli_group=None)


@blueprint.cli.command("seed")
@with_appcontext
@click.argument("seed_file_path", type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def seed_cli(seed_file_path: str):
    seed(seed_file_path)
