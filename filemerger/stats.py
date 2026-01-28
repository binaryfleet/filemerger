from dataclasses import dataclass

@dataclass
class MergeStats:
    files: int = 0
    lines: int = 0
    bytes: int = 0
    skipped_files: int = 0
