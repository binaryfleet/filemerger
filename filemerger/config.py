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

DEFAULT_SEPARATOR_LENGTH = 90
MAX_FILE_SIZE_MB = 2

DEFAULT_OUTPUT_FILE = "filemerger-output.txt"
