from book import utils
from book.pack import BookPack
from book.pack.unpack import BookUnpack

from .test_unpack import unpack_book, clean


def test_pack():
    """Test pack"""
    unpack = unpack_book()

    pack = BookPack(
        book_path=unpack.output_path,
        archive_name="test",
    ).run()

    assert pack.archive_path.exists() is True

    clean(unpack)

    unpack = BookUnpack(pack.archive_path).run()
    assert unpack.output_path.exists() is True
    assert unpack.output_path.is_dir() is True

    if pack.archive_path:
        utils.remove_file(pack.archive_path)

    clean(unpack)
