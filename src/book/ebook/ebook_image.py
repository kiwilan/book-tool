from typing import Any
from ebooklib import epub  # type: ignore
from collections.abc import Buffer


class EbookImage:
    def __init__(self, item: Any):
        image: epub.EpubImage = item  # type: ignore

        self.content: Buffer | None = image.get_content()  # binary # type: ignore
        self.id: str | None = image.get_id()  # cover
        self.name: str = str(image.get_name())  # cover.jpeg
        self.type: int | None = image.get_type()  # 1

    def __str__(self) -> str:
        details = (
            "----------\n"
            f"id: {self.id}\n"
            f"name: {self.name}\n"
            f"type: {self.type}\n"
            "----------\n"
        )
        return f"{details}"
