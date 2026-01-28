import os
import pathspec
from typing import Optional

def load_gitignore(root: str) -> Optional[pathspec.PathSpec]:
    """
    Load .gitignore from the given root directory.
    Returns None if no .gitignore exists.
    """
    gitignore_path = os.path.join(root, ".gitignore")
    if not os.path.isfile(gitignore_path):
        return None

    with open(gitignore_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    return pathspec.PathSpec.from_lines("gitwildmatch", lines)

def is_ignored(
    path: str,
    *,
    root: str,
    spec: Optional[pathspec.PathSpec],
) -> bool:
    if not spec:
        return False

    rel_path = os.path.relpath(path, root)
    return spec.match_file(rel_path)
