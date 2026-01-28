import os
from typing import List, Set
from .filters import is_allowed_file
from .gitignore import load_gitignore
from .user_config import load_user_config
from .config import (
    EXCLUDED_DIRECTORIES,
    DEFAULT_SEPARATOR_LENGTH,
    MAX_FILE_SIZE_MB,
)

def collect_files(
    paths: List[str],
    *,
    output_file: str | None = None,
) -> List[str]:
    collected: Set[str] = set()
    root = os.getcwd()

    gitignore_spec = load_gitignore(root)
    user_config = load_user_config()

    # Resolve config values
    max_mb = user_config.get("filters", {}).get("max_file_size_mb", MAX_FILE_SIZE_MB)
    excluded_dirs = set(EXCLUDED_DIRECTORIES)
    excluded_dirs.update(
        user_config.get("filters", {}).get("exclude_dirs", [])
    )

    max_file_size_bytes = int(max_mb * 1024 * 1024)

    for path in paths:
        if os.path.isfile(path) and is_allowed_file(
            path,
            output_file=output_file,
            gitignore_spec=gitignore_spec,
            root=root,
            max_file_size_bytes=max_file_size_bytes,
            excluded_dirs=excluded_dirs,
        ):
            collected.add(os.path.abspath(path))

        elif os.path.isdir(path):
            for current_root, _, files in os.walk(path):
                for name in sorted(files):
                    full_path = os.path.join(current_root, name)
                    if is_allowed_file(
                        full_path,
                        output_file=output_file,
                        gitignore_spec=gitignore_spec,
                        root=root,
                        max_file_size_bytes=max_file_size_bytes,
                        excluded_dirs=excluded_dirs,
                    ):
                        collected.add(os.path.abspath(full_path))

    return sorted(collected)

def merge_files(files: List[str], output_file: str) -> None:
    user_config = load_user_config()
    sep_len = user_config.get("output", {}).get(
        "separator_length", DEFAULT_SEPARATOR_LENGTH
    )
    separator = "-" * int(sep_len)

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("FILES INCLUDED\n")
        out.write(separator + "\n")
        for f in files:
            out.write(f"{f}\n")
        out.write("\n")

        for file_path in files:
            out.write(separator + "\n")
            out.write(f"FILE: {file_path}\n")
            out.write(separator + "\n")

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    out.write(f.read().rstrip() + "\n")
            except UnicodeDecodeError:
                out.write("[Skipped: binary or non-UTF8 file]\n")
