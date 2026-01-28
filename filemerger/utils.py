import os
from .config import DEFAULT_OUTPUT_FILE

def normalize_output_filename(output: str | None) -> str:
    """
    Normalize output filename:
    - Default to DEFAULT_OUTPUT_FILE
    - Force .txt extension
    - Strip directory components (always write to CWD)
    """
    if not output:
        return DEFAULT_OUTPUT_FILE

    base = os.path.basename(output)
    name, ext = os.path.splitext(base)

    if ext.lower() != ".txt":
        return f"{name}.txt"

    return base
