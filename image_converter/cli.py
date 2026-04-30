#!/usr/bin/env python3

import sys
from pathlib import Path


from .validators import validate_paths
from .globals import DEFAULT_QUALITIES
from .parser import parser
from .converters import convert_file, convert_folder_content


def main():
    args = parser.parse_args()
    paths = [Path(p) for p in args.paths]
    output_format = args.format.lower()
    if output_format == "jpg":
        output_format = "jpeg"

    quality = args.quality if args.quality else DEFAULT_QUALITIES[output_format]
    output_dir = Path(args.output) if args.output else None

    if not validate_paths(paths):
        sys.exit()

    for path in paths:
        if path.is_dir():
            convert_folder_content(
                folder_path=path,
                output_format=output_format,
                quality=quality,
                output_dir=output_dir,
            )
        elif path.is_file():
            status = convert_file(
                file_path=path,
                output_format=output_format,
                quality=quality,
                output_dir=output_dir,
            )
            print(f"STATUS: {status['status']}, FILE: {status['file']}")


if __name__ == "__main__":
    main()
