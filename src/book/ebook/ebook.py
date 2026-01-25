import os
from pathlib import Path
from typing import Any
import collections.abc
from datetime import datetime
import ebooklib  # type: ignore
from ebooklib import epub  # type: ignore
from .ebook_meta import EbookMeta
from .ebook_identifier import EbookIdentifier
from .ebook_image import EbookImage


class Ebook:
    def __init__(self, path: str):
        self.path = path
        self.title: str | None = None
        self.language: str | None = None
        self.creators: list[str] | None = []
        self.description: str | None = None
        self.publisher: str | None = None
        self.identifiers: list[EbookIdentifier] = []
        self.subjects: list[str] | None = None
        self.published_at: datetime | None = None
        self.meta: list[EbookMeta] = []
        self.series: str | None = None
        self.volume: float | None = None
        self.identifier_isbn: str | None = None
        self.identifier_amazon: str | None = None
        self.identifier_uuid: str | None = None
        self.identifier_calibre: str | None = None
        self.title_sort: str | None = None
        self.created_at: datetime | None = None
        self.rating: float | None = None
        self.images: list[EbookImage] = []

        if not Path(path):
            print("File not exists!")

        self._instance = epub.read_epub(self.path)  # type: ignore

        self._parse()
        self._cover()

    def save_cover(self):
        cover = self.images[0] if len(self.images) > 0 else None
        if not cover:
            print("No cover!")

        if cover and cover.content:
            path = os.path.basename(cover.name)
            with open(path, "wb") as f:
                f.write(cover.content)

    def get_identifier(self, scheme: str):
        identifier: str | None = None
        for i in self.identifiers:
            if i.scheme == scheme:
                identifier = i.value

        return identifier

    def get_meta(self, name: str):
        meta: str | None = None
        for i in self.meta:
            if i.name == name:
                meta = i.value

        return meta

    def _cover(self):
        items = self._instance.get_items_of_type(ebooklib.ITEM_IMAGE)  # type: ignore
        for item in items:  # type: ignore
            self.images.append(EbookImage(item))

    def _parse(self):
        try:
            self.title = self._extract_str("title")
            self.language = self._extract_str("language")
            self.creators = self._extract_list_str("creator")
            self.description = self._extract_str("description")
            self.publisher = self._extract_str("publisher")
            self.subjects = self._extract_list_str("subject")
            published_at = self._extract_str("date")
            if published_at:
                self.published_at = datetime.fromisoformat(str(published_at))
            self._extract_identifiers()
            self._extract_meta()
            self.series = self.get_meta("calibre:series")
            volume = self.get_meta("calibre:series_index")
            if volume:
                self.volume = float(volume)
            self.identifier_isbn: str | None = self.get_identifier("isbn")
            self.identifier_amazon: str | None = self.get_identifier("amazon")
            self.identifier_uuid: str | None = self.get_identifier("uuid")
            self.identifier_calibre: str | None = self.get_identifier("calibre")
            self.title_sort: str | None = self.get_meta("calibre:title_sort")
            created_at = self.get_meta("calibre:timestamp")
            if created_at:
                self.created_at = datetime.fromisoformat(str(created_at))
            rating = self.get_meta("calibre:rating")
            if rating:
                self.rating = float(rating)

        except Exception as e:
            print(f"Erreur lors de la lecture : {e}")

    def _extract(self, name: str, namespace: str = "DC") -> Any:
        return self._instance.get_metadata(namespace, name)  # type: ignore

    def _extract_str(self, name: str, namespace: str = "DC") -> str | None:
        value = self._extract(name, namespace)
        if isinstance(value, collections.abc.Sequence):
            return value[0][0]  # type: ignore

        return None

    def _extract_identifiers(self):
        values = self._extract("identifier")
        for value in values:
            self.identifiers.append(EbookIdentifier(value))

    def _extract_meta(self):
        for namespace, tags in self._instance.metadata.items():  # type: ignore # pylint: disable=unused-variable
            if "meta" in tags:
                for corps, attributs in tags["meta"]:  # type: ignore # pylint: disable=unused-variable
                    self.meta.append(EbookMeta(attributs))

    def _extract_list_str(self, name: str):
        items: list[str] = []

        values = self._extract(name)
        for value in values:
            try:
                _ = value[0]
                iter(value)
                v: str = str(value[0])
                items.append(v.strip().capitalize())
            except (TypeError, IndexError, KeyError):
                continue

        if items:
            return items

        return None

    def __str__(self) -> str:
        details = (
            "----------\n"
            f"path: {self.path}\n"
            f"title: {self.title}\n"
            f"language: {self.language}\n"
            f"creators: {self.creators}\n"
            f"description: {self.description}\n"
            f"publisher: {self.publisher}\n"
            f"identifiers: {len(self.identifiers)} items\n"
            f"subjects: {self.subjects}\n"
            f"published_at: {self.published_at}\n"
            f"meta: {len(self.meta)} items\n"
            f"series: {self.series}\n"
            f"volume: {self.volume}\n"
            f"identifier_isbn: {self.identifier_isbn}\n"
            f"identifier_amazon: {self.identifier_amazon}\n"
            f"identifier_uuid: {self.identifier_uuid}\n"
            f"identifier_calibre: {self.identifier_calibre}\n"
            f"title_sort: {self.title_sort}\n"
            f"created_at: {self.created_at}\n"
            f"rating: {self.rating}\n"
            f"images: {len(self.images)} items\n"
            "----------\n"
        )
        return f"{details}"
