from typing import Any


class EbookIdentifier:
    # <dc:identifier opf:scheme="ISBN">9782070309597</dc:identifier>
    # <dc:identifier opf:scheme="AMAZON">2277232629</dc:identifier>
    # <dc:identifier id="uuid_id" opf:scheme="uuid">25f65cf1-4f6e-4bac</dc:identifier>
    # <dc:identifier opf:scheme="calibre">25f65cf1-4f6e-4bac-9501-2dac69cca495</dc:identifier>
    def __init__(self, value: Any):
        identifier_value = value[0]
        scheme_dict = value[1]
        identifier_scheme = scheme_dict.get("{http://www.idpf.org/2007/opf}scheme")

        scheme = str(identifier_scheme)
        if not scheme:
            return

        self.scheme = scheme.lower()
        self.value = str(identifier_value)

    def __str__(self) -> str:
        details = (
            "----------\n"
            f"scheme: {self.scheme}\n"
            f"value: {self.value}\n"
            "----------\n"
        )
        return f"{details}"
