"""Utility functions for Breeze CLI tool."""

import os
import logging
from pathlib import Path
from typing import Optional, List


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=level,
        format=format_string,
        handlers=[
            logging.StreamHandler(),
        ]
    )


def validate_file_path(file_path: str) -> bool:
    """Validate that a file path exists and is a Python file."""
    path = Path(file_path)
    return path.exists() and path.is_file() and path.suffix == ".py"


def read_file_content(file_path: str) -> str:
    """Read content from a file safely."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to read file '{file_path}': {e}")


def write_file_content(file_path: str, content: str) -> None:
    """Write content to a file safely."""
    try:
        # Create directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        raise RuntimeError(f"Failed to write file '{file_path}': {e}")


def get_output_filename(original_path: str, command: str) -> str:
    """Generate appropriate output filename based on command."""
    path = Path(original_path)
    
    extensions = {
        "doc": ".documented.py",
        "summarize": ".summary.md",
        "test": f"test_{path.stem}.py",
        "inspect": ".inspection.md",
        "refactor": ".refactored.py",
        "annotate": ".annotated.py",
        "migrate": ".migrated.py"
    }
    
    extension = extensions.get(command, ".output.txt")
    
    if command == "test":
        # Put test files in a tests directory
        test_dir = path.parent / "tests"
        test_dir.mkdir(exist_ok=True)
        return str(test_dir / f"test_{path.stem}.py")
    else:
        return str(path.parent / f"{path.stem}{extension}")


def get_api_key() -> Optional[str]:
    """Get the Gemini API key from environment variables."""
    return os.getenv("GEMINI_API_KEY")


def format_error_message(error: Exception, context: str = "") -> str:
    """Format error messages for user display."""
    error_type = type(error).__name__
    error_msg = str(error)
    
    if context:
        return f"Error in {context}: {error_type} - {error_msg}"
    else:
        return f"{error_type}: {error_msg}"


def extract_python_code(text: str) -> str:
    """Extract Python code from text that might contain markdown code blocks."""
    import re
    
    # Look for code blocks
    code_block_pattern = r'``````'
    matches = re.findall(code_block_pattern, text, re.DOTALL)
    
    if matches:
        return matches[0]
    
    # If no code blocks found, return original text
    return text


def count_lines_of_code(content: str) -> dict:
    """Count various metrics for code content."""
    lines = content.splitlines()
    
    total_lines = len(lines)
    blank_lines = sum(1 for line in lines if not line.strip())
    comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
    code_lines = total_lines - blank_lines - comment_lines
    
    return {
        "total_lines": total_lines,
        "code_lines": code_lines,
        "comment_lines": comment_lines,
        "blank_lines": blank_lines
    }


def create_backup(file_path: str) -> str:
    """Create a backup of a file before modification."""
    path = Path(file_path)
    backup_path = path.with_suffix(f"{path.suffix}.backup")
    
    if path.exists():
        import shutil
        shutil.copy2(path, backup_path)
        return str(backup_path)
    
    return ""


def list_python_files(directory: str) -> List[str]:
    """List all Python files in a directory."""
    path = Path(directory)
    if not path.exists() or not path.is_dir():
        return []
    
    return [str(f) for f in path.rglob("*.py")]


def get_project_info(directory: str) -> dict:
    """Get basic information about a Python project."""
    path = Path(directory)
    if not path.exists():
        return {}
    
    info = {
        "directory": str(path),
        "python_files": list_python_files(directory),
        "has_setup_py": (path / "setup.py").exists(),
        "has_pyproject_toml": (path / "pyproject.toml").exists(),
        "has_requirements_txt": (path / "requirements.txt").exists(),
        "has_tests": bool(list(path.rglob("test*.py")))
    }
    
    return info
