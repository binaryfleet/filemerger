import os
from .config import (
    ALLOWED_EXTENSIONS,
    EXCLUDED_DIRECTORIES,
    EXCLUDED_FILES,
    MAX_FILE_SIZE_BYTES,
)
from .gitignore import is_ignored

def is_allowed_file(
    path: str,
    *,
    output_file: str | None = None,
    gitignore_spec=None,
    root: str | None = None,
) -> bool:
    if not os.path.isfile(path):
        return False

    if output_file and os.path.abspath(path) == os.path.abspath(output_file):
        return False

    if gitignore_spec and root and is_ignored(path, root, gitignore_spec):
        return False

    if os.path.basename(path) in EXCLUDED_FILES:
        return False

    if os.path.splitext(path)[1].lower() not in ALLOWED_EXTENSIONS:
        return False

    parts = path.split(os.sep)
    if any(part in EXCLUDED_DIRECTORIES for part in parts):
        return False

    try:
        if os.path.getsize(path) > MAX_FILE_SIZE_BYTES:
            return False
    except OSError:
        return False

    return True
