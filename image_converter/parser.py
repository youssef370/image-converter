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

parser.add_argument("--quality", "-q", type=int, help="Quality of the output file. Valid ranges: JPEG (0-100), AVIF (0-63), WEBP (0-100), PNG (0-9)")

parser.add_argument("--output", "-o", type=str, help="Destination folder for the converted files")

parser.add_argument("--recursive", "-r", action="store_true", help="Apply conversion to image files in subdirectories and recreate folder structure in output directory")

parser.add_argument("--no-cache", "-nc", action="store_true", help="Ignore cache and convert all files")
