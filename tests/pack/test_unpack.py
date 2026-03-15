from book import utils
from book.pack import BookUnpack
from tests.test_files import EPUB_TEST_FILE, copy_to_output


def test_unpack():
    """Test unpack"""
    unpack = unpack_book()
    # clean(unpack)


def unpack_book():
    test_file = copy_to_output(EPUB_TEST_FILE)
    unpack = BookUnpack(test_file).run()

    assert unpack.output_path.exists() is True
    assert unpack.output_path.is_dir() is True

    return unpack


def clean(unpack: BookUnpack):
    utils.remove_directory(unpack.output_path)
    utils.remove_file(unpack.book_path)
