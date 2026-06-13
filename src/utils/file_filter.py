from pathlib import Path

def file_filter(file_path: str) -> bool:
    path = Path(file_path)

    # Ignore directories
    ignored_dirs = {
        ".git",
        ".github",
        "__pycache__",
        ".venv",
        "venv",
        "env",
        "node_modules",
        "dist",
        "build",
        ".next",
        ".turbo",
        ".cache",
        "coverage",
        ".idea",
        ".vscode",
    }

    if any(part in ignored_dirs for part in path.parts):
        return False

    # Ignore file extensions
    ignored_extensions = {
        ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
        ".pdf", ".zip", ".tar", ".gz", ".rar",
        ".mp4", ".mp3", ".wav",
        ".exe", ".dll", ".so", ".dylib",
        ".pyc", ".pyo",
        ".lock",
    }

    if path.suffix.lower() in ignored_extensions:
        return False

    # Ignore specific files
    ignored_files = {
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "poetry.lock",
        ".env",
        ".env.local",
        ".gitignore"
    }

    if path.name in ignored_files:
        return False

    return True