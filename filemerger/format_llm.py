from typing import List
from .stats import MergeStats

class LLMFormatter:
    def __init__(self, *, compact: bool = False):
        self.compact = compact

    def write(self, files: List[str], output_file: str) -> MergeStats:
        stats = MergeStats(files=len(files))

        with open(output_file, "w", encoding="utf-8") as out:
            for idx, file_path in enumerate(files, start=1):
                header = f"[{idx}] {file_path}\n"
                out.write(header)
                stats.lines += 1
                stats.bytes += len(header.encode("utf-8"))

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read().rstrip() + ("\n" if self.compact else "\n\n")
                        out.write(content)
                        stats.lines += content.count("\n")
                        stats.bytes += len(content.encode("utf-8"))
                except UnicodeDecodeError:
                    skipped = "[Skipped: binary or non-UTF8 file]\n"
                    out.write(skipped)
                    stats.lines += 1
                    stats.bytes += len(skipped.encode("utf-8"))
                    stats.skipped_files += 1

                if not self.compact:
                    out.write("\n")
                    stats.lines += 1
                    stats.bytes += 1

        return stats
