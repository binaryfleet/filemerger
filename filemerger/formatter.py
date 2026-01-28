from typing import List
from .stats import MergeStats

class BaseFormatter:
    def write(self, files: List[str], output_file: str) -> MergeStats:
        raise NotImplementedError
