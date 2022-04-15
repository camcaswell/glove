
from pathlib import Path

# click.get_app_dir to auto-get an appropriate user config location

GLOVE_INTERNAL = Path("./glove-internal")
TEMP_DIR = GLOVE_INTERNAL / "temp"
TEMPLATES_DIR = GLOVE_INTERNAL / "subjects" / "templates"
META_DIR = GLOVE_INTERNAL / "subjects" / "meta"