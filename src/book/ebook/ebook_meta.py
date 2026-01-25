from typing import Any


class EbookMeta:
    # <meta name="calibre:title_sort" content="Légion de l'espace, La"/>
    # <meta name="calibre:series" content="Ceux de la Légion"/>
    # <meta name="calibre:series_index" content="1"/>
    # <meta name="calibre:timestamp" content="2026-01-25T07:55:38.601373+00:00"/>
    # <meta name="calibre:rating" content="6.00"/>
    # <meta name="cover" content="cover"/>
    def __init__(self, attributs: Any):
        name = str(attributs.get("name"))  # type: ignore
        if not name:
            return

        self.name = name.lower()
        self.value = str(attributs.get("content"))  # type: ignore

    def __str__(self) -> str:
        details = (
            "----------\n"
            f"name: {self.name}\n"
            f"value: {self.value}\n"
            "----------\n"
        )
        return f"{details}"
