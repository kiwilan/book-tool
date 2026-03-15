import shutil
import zipfile
from pathlib import Path
from book import utils
from book.common import AutoRepr


class BookPack(AutoRepr):
    archive_path: Path

    def __init__(self, book_path: str | Path, archive_name: str | None = None):
        self.book_path: Path = Path(book_path).resolve()
        if not self.book_path.exists():
            raise FileNotFoundError(f"{book_path} not found")

        if not self.book_path.is_dir():
            raise FileNotFoundError(f"{book_path} is not directory")

        # cwd = Path(os.getcwd()).resolve()
        self.output_path: Path = self.book_path.parent
        if archive_name:
            self.archive_name = archive_name
        else:
            self.archive_name: str = self.book_path.stem
        self.extension: str = "epub"

    def run(self):
        self._pack_shutil()

        return self

    def _pack_shutil(self):
        archive_path = shutil.make_archive(
            base_name=str(self.output_path / self.archive_name),
            format="zip",
            root_dir=self.book_path,
        )
        archive_path = utils.change_extension(
            absolute_path=archive_path,
            new_extension=self.extension,
            overwrite=True,
        )
        self.archive_path = Path(archive_path).resolve()

    def _pack_path(self):
        # 1. Vérifier que la source existe
        if not self.book_path.exists():
            raise FileNotFoundError(f"Source introuvable : {self.book_path}")

        # 2. Créer le dossier de destination si besoin
        self.output_path.mkdir(parents=True, exist_ok=True)

        self.archive_path: Path = (
            self.output_path / f"{self.archive_name}.{self.extension}"
        )

        print(f"Création de l'archive vers : {self.archive_path}")

        with zipfile.ZipFile(self.archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
            files_found = False
            for file_path in self.book_path.rglob("*"):
                if file_path.is_file():
                    files_found = True
                    print(f"Compression de : {file_path.name}")
                    archive.write(
                        file_path, arcname=file_path.relative_to(self.book_path)
                    )

            if not files_found:
                print("Attention : Aucun fichier trouvé dans le dossier source !")
