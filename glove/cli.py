import os
import shutil
import sys
from pathlib import Path

import click
import yaml

import glove.config as cfg
import glove.util as util


@click.group()
def cli():
    pass

@cli.command(name="hold")
@click.argument("file", type=click.Path())
@click.option("-n", "--name", type=str)
def hold(file: str, name: str = None):
    """
    Start tracking a file.

    Args:
        file (_type_): _description_
    """
    print(file, type(file))
    print(os.getcwd())

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


@cli.command(name="clean")
def clean():
    for folder in (cfg.META_DIR, cfg.TEMPLATES_DIR):
        for file in os.listdir(folder):
            os.remove(folder / file)
    click.echo("Cleaned :)")





if __name__ == "__main__":
    cli()
