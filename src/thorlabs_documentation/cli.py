import argparse
import logging
import os
import pathlib
import thorlabs_documentation as td


def fetch_many():
    parser = argparse.ArgumentParser(
        "fetch all documents related to the given part numbers"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print debug-level information"
    )
    parser.add_argument(
        "-a",
        "--from-file",
        type=str,
        help="Read part numbers from the specified file, with one part number per line",
    )
    parser.add_argument(
        "-d",
        "--data-dir",
        type=str,
        help="Directory where documents are stored. By default, this is the current working directory.",
        default=pathlib.Path.cwd() / "thorlabs",
    )
    parser.add_argument(
        "part_numbers", nargs="*", help="Space-separated list of part numbers to fetch"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    if args.from_file:
        part_numbers = list(map(str.strip, open(args.from_file, "r").splitlines()))
    else:
        part_numbers = args.part_numbers

    if len(part_numbers) == 0:
        return

    logging.debug(f"Fetching {len(part_numbers)} parts")

    for part_number in part_numbers:
        td.fetch_documents_for_part(part_number, args.data_dir)
