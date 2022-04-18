
import os
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Optional
from uuid import uuid4

import click
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
        match re.split(r"([-.])", template_filename):
        case (id_, ".", "glove") if i
        id_, _, name = template_filename.partition("-")
        subject_identifiers[id_] = name or None
    return subject_identifiers

