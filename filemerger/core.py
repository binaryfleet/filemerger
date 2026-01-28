import os
from typing import List, Set, Tuple
from .filters import is_allowed_file
from .gitignore import load_gitignore
from .user_config import load_user_config
from .config import (
    EXCLUDED_DIRECTORIES,
    DEFAULT_SEPARATOR_LENGTH,
    MAX_FILE_SIZE_MB,
)
from .stats import MergeStats

def collect_files(
    paths: List[str],
    *,
    output_file: str | None = None,
) -> List[str]:
    collected: Set[str] = set()
    root = os.getcwd()

    gitignore_spec = load_gitignore(root)
    user_config = load_user_config()

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

def merge_files(files: List[str], output_file: str) -> MergeStats:
    user_config = load_user_config()
    sep_len = user_config.get("output", {}).get(
        "separator_length", DEFAULT_SEPARATOR_LENGTH
    )
    separator = "-" * int(sep_len)

    stats = MergeStats(files=len(files))

    with open(output_file, "w", encoding="utf-8") as out:
        header = "FILES INCLUDED\n" + separator + "\n"
        out.write(header)
        stats.lines += header.count("\n")
        stats.bytes += len(header.encode("utf-8"))

        for f in files:
            line = f"{f}\n"
            out.write(line)
            stats.lines += 1
            stats.bytes += len(line.encode("utf-8"))

        out.write("\n")
        stats.lines += 1
        stats.bytes += 1

        for file_path in files:
            block_header = (
                f"{separator}\nFILE: {file_path}\n{separator}\n"
            )
            out.write(block_header)
            stats.lines += block_header.count("\n")
            stats.bytes += len(block_header.encode("utf-8"))

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().rstrip() + "\n"
                    out.write(content)
                    stats.lines += content.count("\n")
                    stats.bytes += len(content.encode("utf-8"))
            except UnicodeDecodeError:
                skipped = "[Skipped: binary or non-UTF8 file]\n"
                out.write(skipped)
                stats.lines += 1
                stats.bytes += len(skipped.encode("utf-8"))
                stats.skipped_files += 1

    return stats
