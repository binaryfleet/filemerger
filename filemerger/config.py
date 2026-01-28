ALLOWED_EXTENSIONS = {
    ".py", ".js", ".json", ".html", ".css", ".txt", ".md"
}

EXCLUDED_FILES = {
    ".DS_Store",
}

EXCLUDED_DIRECTORIES = {
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    "node_modules",
    "migrations",
    "tests",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "env",
    ".env",
    ".venv",
}

DEFAULT_SEPARATOR = "-" * 90
MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024  # 2 MB

DEFAULT_OUTPUT_FILE = "filemerger-output.txt"
