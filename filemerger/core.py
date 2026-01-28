import os
from typing import List, Set
from .filters import is_allowed_file
from .config import DEFAULT_SEPARATOR
from .gitignore import load_gitignore

def collect_files(
    paths: List[str],
    *,
    output_file: str | None = None,
) -> List[str]:
    collected: Set[str] = set()

    root = os.getcwd()
    gitignore_spec = load_gitignore(root)

    for path in paths:
        if os.path.isfile(path) and is_allowed_file(
            path,
            output_file=output_file,
            gitignore_spec=gitignore_spec,
            root=root,
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
                    ):
                        collected.add(os.path.abspath(full_path))

    return sorted(collected)

def merge_files(files: List[str], output_file: str) -> None:
    with open(output_file, "w", encoding="utf-8") as out:
        out.write("FILES INCLUDED\n")
        out.write(DEFAULT_SEPARATOR + "\n")
        for f in files:
            out.write(f"{f}\n")
        out.write("\n")

        for file_path in files:
            out.write(DEFAULT_SEPARATOR + "\n")
            out.write(f"FILE: {file_path}\n")
            out.write(DEFAULT_SEPARATOR + "\n")

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    out.write(f.read().rstrip() + "\n")
            except UnicodeDecodeError:
                out.write("[Skipped: binary or non-UTF8 file]\n")
