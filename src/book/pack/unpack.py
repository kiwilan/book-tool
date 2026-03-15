import zipfile
from pathlib import Path
from book import utils
from book.common import AutoRepr


class BookUnpack(AutoRepr):
    def __init__(self, book_path: str | Path):
        self.book_path: Path = Path(book_path).resolve()
        if not self.book_path.exists():
            raise FileNotFoundError(f"{book_path} not found")

        # cwd = Path(os.getcwd()).resolve()
        output: Path = self.book_path.parent
        name: str = self.book_path.stem

        self.output_path: Path = output / name

    def run(self):
        self._unpack()

        return self

    def _unpack(self):
        utils.make_directory(self.output_path)
        with zipfile.ZipFile(self.book_path, "r") as zip_ref:
            zip_ref.extractall(self.output_path)
