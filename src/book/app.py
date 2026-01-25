"""book-tool main"""

import argparse
import sys
import logging
from .args import BookArgs

# from .command import CommandBuild
from .env import python_check
from .command.fetch import fetch_api

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)


def main() -> None:
    """book-tool main"""
    parser = argparse.ArgumentParser(
        prog="book-tool",
        description="CLI to handle books",
    )

    args = BookArgs(parser)
    # python_check()

    # print("")
    # print(parser.prog)
    # print(parser.description)
    # print(f"Execute command {args.command}...\n")

    try:
        print("book-tool")
        # if args.command == "audible":
        #     CommandAudible(args)
        # elif args.command == "build":
        #     CommandBuild(args)
        fetch_api(args)
    except Exception as e:
        logging.getLogger("book.cli").error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
