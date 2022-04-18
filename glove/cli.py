import os
import shutil
import sys
from pathlib import Path

import click
import yaml

import glove.config as cfg
import glove.util as util


CONTEXT_SETTINGS = {
    "help_option_names": ["--help", "-h"],
    "token_normalize_func": lambda token: token.lower().strip(),
}


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

@cli.command(name="grab")
@click.argument("file", type=click.Path())
@click.option("-n", "--name", type=str)
def grab(file: str, name: str = None):
    """
    Start tracking a file.

    Args:
        file (_type_): _description_
    """

    file_path = Path(file).resolve()

    with click.open_file(file_path) as source:
        source_content = source.read()

    subject_identifier = subject_id = util.generate_subject_id()
    if name is not None:
        subject_identifier = f"{subject_id}-{name}"

    with open(cfg.TEMPLATES_DIR / f"{subject_identifier}.glove", "w") as template:
        template.write(source_content)

    meta_data = {subject_id: {
        "name": name,
        "deploy_target": str(file_path),
        "substitutions": {},
    }}
    with open(cfg.META_DIR / f"{subject_identifier}.yml", "w") as meta_file:
        yaml.dump(meta_data, meta_file, default_flow_style=False)


@cli.command(name="wipe")
def wipe():
    """
    Dev only, clear out glove-internal/subjects/templates and glove-internal/subjects/meta
    """
    for folder in (cfg.META_DIR, cfg.TEMPLATES_DIR):
        for file in os.listdir(folder):
            os.remove(folder / file)
    click.echo("Cleaned :)")





if __name__ == "__main__":
    cli()
