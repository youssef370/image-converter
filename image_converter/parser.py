from argparse import ArgumentParser

from .globals import SUPPORTED_FORMATS

parser = ArgumentParser()
parser.add_argument("paths", nargs="+", help="Files or directories to process")

parser.add_argument(
        "--format", "-f",
        help="Output format",
        choices=SUPPORTED_FORMATS,
        default="webp",
    )

parser.add_argument("--quality", "-q", type=int, help="Quality of the output file")

parser.add_argument("--output", "-o", type=str, help="Destination folder for the converted files")


