
from pathlib import Path

# click.get_app_dir to auto-get an appropriate user config location

GLOVE_INTERNAL = Path("C:/Code/glove/glove-internal")
TEMP_DIR = GLOVE_INTERNAL / "temp"
TEMPLATES_DIR = GLOVE_INTERNAL / "subjects" / "templates"
META_DIR = GLOVE_INTERNAL / "subjects" / "meta"


SUBJECT_ID_PATTERN = r"[0-9a-fA-F]{8}"
SUBJECT_FILE_NAME = r"[0-9a-zA-Z\-=._+*?!><,;`'\"\[\]{}|()@#$%^&]+"
