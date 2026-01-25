from book.args import BookArgs
from book.ebook import Ebook


def fetch_api(args: BookArgs):
    # fetch(args)
    if args.epub_path:
        ebook = Ebook(args.epub_path)
        print(ebook)
        ebook.save_cover()
