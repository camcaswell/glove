
from uuid import uuid4
from pathlib import Path
import os
import glove.config as cfg

def generate_subject_id() -> str:
    """
    Generate a unique ID for a subject file.

    Returns:
        str: 8-digit hex string
    """
    current_ids = get_subject_ids()
    while (candidate := uuid4().hex[-8:]) in current_ids:
        pass
    return candidate


def get_subject_ids() -> set[str]:
    """
    Scans glove-internal/subjects/templates and parses our IDs from the filenames.

    Returns:
        set[str]: The IDs of the current subject files. 
    """
    return {template_name.partition("-")[0] for template_name in os.listdir(cfg.TEMPLATES_DIR)}