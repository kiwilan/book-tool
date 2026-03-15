from pathlib import Path
from book import utils

EPUB_TEST_FILE = "tests/media/epub-test.epub"
OUTPUT_PATH = "tests/media/output"


def output_path(file_path: str) -> Path:
    """Get full output path"""
    new_path = f"{OUTPUT_PATH}/{file_path}"
    new_path = Path(new_path).resolve()

    return new_path


def copy_to_output(path: Path | str) -> Path:
    """Copy directory or file to `OUTPUT_PATH`"""
    if isinstance(path, str):
        path = Path(path)
    path = path.resolve()
    if path.is_dir():
        return utils.copy_directory(path, output_path(path.name))

    if path.is_file():
        return utils.copy_file(path, output_path(path.name))

    raise FileNotFoundError(f"Error on {path}")
