
import os
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Optional
from uuid import uuid4

import click
from click.core import Argument, Context

import glove.config as cfg


def generate_subject_id(reserved: Iterable[str] = tuple()) -> str:
    """
    Generate a unique ID for a subject file.

    Args:
        reserved (Iterable[str]): Iterable of strings to be added to collision check

    Returns:
        str: 8-digit hex string
    """
    reserved = set(reserved)
    reserved |= get_subject_identifiers().keys()
    while (candidate := uuid4().hex[-8:]) in reserved:
        pass
    return candidate


def get_subject_identifiers() -> dict[str, Optional[str]]:
    """
    Scans glove-internal/subjects/templates and parses IDs and names from filenames.

    Returns:
        dict[str, Optional[str]]: The IDs as keys, with names as values if they exist, else None
    """
    subject_identifiers = {}
    for template_filename in os.listdir(cfg.TEMPLATES_DIR):
        id_, name = parse_template_filename(template_filename)
        subject_identifiers[id_] = name or None
    return subject_identifiers

def resolve_subject_refs(ctx: Context, arg: Argument, subject_refs: tuple[str]) -> set[str]:
    """
    Search existing subjects to resolve references into ids.

    Args:
        ctx (Context): Click command context
        arg (Argument): Click argument
        subject_refs (tuple[str]): References to subjects

    Returns:
        set[str]: The ids of the referenced subjects
    """
    found = set()
    bad = []
    ids = get_subject_identifiers()
    names = {name.lower(): id_ for id_,name in ids.items() if name is not None}
    for subject_ref in subject_refs:
        if subject_ref in ids:
            found.add(subject_ref)
        elif subject_ref in names:
            found.add(names[subject_ref])
        else:
            bad.append(subject_ref)
    if bad:
        bad_refs = "\n".join(bad)
        raise click.BadParameter(f"Did not recognize these references to subject files:\n{bad_refs}")
    else:
        return found

def parse_template_filename(filename: str) -> tuple[Optional[str], Optional[str]]:
    """
    Parse a subject template filename to get the id and name.
    Can be used to validate as well, since this returns None for the id if invalid. 

    Args:
        filename (str): Name of a subject template file

    Returns:
        tuple[Optional[str], Optional[str]]: The id and name of the subject
    """
    pat = fr"(?P<id_>{cfg.SUBJECT_ID_PATTERN})(?:-(?P<name>{cfg.SUBJECT_FILE_NAME}))?\.glove$"
    m = re.match(pat, filename)
    if m is None:
        return None, None
    else:
        return m.group("id_"),  m.group("name")
