import argparse
import sys
from pathlib import Path
from PIL import Image

parser = argparse.ArgumentParser()

FORMATS = {
    "jpeg": {
        "encoder": encode_jpeg,
        "quality": 75,
    },
    "avif": {
        "encoder": encode_avif,
        "quality": 85,
    },
    "webp": {
        "encoder": encode_webp,
        "quality": 80,
    },
    "png": {
        "encoder": encode_png,
        "quality": 75,
    },
}

SUPPORTED_FORMATS = set(FORMATS.keys())

ENCODERS = {k: v["encoder"] for k, v in FORMATS.items()}

DEFAULT_QUALITIES = {k: v["quality"] for k, v in FORMATS.items()}

def encode_avif(img: Image, quality: int, output_dir: Path):
    """Encode image file to AVIF
    Args:
        img: Image object to convert to AVIF
        quality: Compression quality inputted by user, if no input then quality=85
        output_dir: Directory where output file will be written
    Returns:
        str: path of the output file
    """
    name = Path(img.filename).stem if img.filename else "output"
    output = output_dir / f"{name}.avif"
    img.save(output, format="AVIF", quality=max(30, int(quality * 0.7)))

    return output


def encode_webp(img: Image, quality: int, output_dir: Path):
    """Encode image file to WEBP
    Args:
        img: Image object to convert to WEBP
        quality: Compression quality inputted by user, if no input then quality=75
        output_dir: Directory where output file will be written
    Returns:
        str: path of the output file
    """
    name = Path(img.filename).stem if img.filename else "output"
    output = output_dir / f"{name}.webp"
    img.save(output, format="WEBP", quality=quality, method=6)

    return output


def encode_jpeg(img: Image, quality: int, output_dir: Path):
    """Encode image file to JPEG
    Args:
        img: Image object to convert to JPEG
        quality: Compression quality inputted by user, if no input then quality=75
        output_dir: Directory where output file will be written
    Returns:
        str: path of the output file
    """
    name = Path(img.filename).stem if img.filename else "output"
    output = output_dir / f"{name}.jpeg"
    img.save(
        output,
        format="JPEG",
        quality=quality,
        optimize=True,
        progressive=True,
    )

    return output


def encode_png(img: Image, quality: int, output_dir: Path):
    """Encode image file to PNG
    Args:
        img: Image object to convert to JPEG
        quality: Compression quality inputted by user, if no input then quality=75
        output_dir: Directory where output file will be written
    Returns:
        str: path of the output file
    """
    compression = round((quality / 100) * 9)
    name = Path(img.filename).stem if img.filename else "output"
    output = output_dir / f"{name}.png"

    img.convert("RGBA").save(output, format="PNG", compress_level=compression)

    return output


def convert_file(*, file_path: Path, output_format: str, quality: int):
    """Create the output directory and execute the encoding function based user's format input
    Args:
        file_path: Path of the file to convert
        format: Format to which the input file should be converted
        quality: Compression quality inputted by user, if no input then depends on the output file format
    Returns:
        str: Path to the output file
    """
    if not validate_file(file_path):
        return {"status": "invalid", "file": str(file_path)}

    output_dir = file_path.parent / "converted"
    output_dir.mkdir(parents=True, exist_ok=True)

    ext = output_format
    try:
        with Image.open(file_path) as img:
            output = ENCODERS[ext](img, quality, output_dir)
            return {"status": "ok", "file": output}
    except Exception:
        print("Cannot open image")
        return {"status": "failed", "file": str(file_path)}


def convert_folder_content(*, folder_path: Path, quality: int, output_format: str):
    """Converts image files within a folder.
    Args:
        folder_path: Path of the folder the content of which should be converted.
        quality: Compression quality inputted by user, if no input then depends on the output file format
    """
    for file in folder_path.iterdir():
        if file.is_file():
            status = convert_file(
                file_path=file, output_format=output_format, quality=quality
            )
            print(f"STATUS: {status['status']}, FILE: {status['file']}")


def validate_file(file_path: Path):
    """Checks if input file is one of the supported types
    Args:
        file_path: Path to the file to check
    Returns:
        bool: true if the file is supported, otherwise false
    """

    ext = file_path.suffix.lstrip(".").lower()
    if ext not in SUPPORTED_FORMATS:
        print(
            f"File type not supported. Should be in one of the following formats: {', '.join(SUPPORTED_FORMATS)}"
        )
        return False
    return True


def validate_paths(paths: list[str]):
    """Checks if the paths inputted by the user are valid. If one of them isn't, the program stops.
    Args:
        paths: list of paths to validate
    Returns:
        bool: True if all paths are valid, otherwise False
    """
    for path in paths:
        p = Path(path)
        if not p.exists():
            print(f"{path} is not a valid path.")
            return False
    return True


def main():
    parser.add_argument("paths", nargs="+", help="Files or directories to process")

    parser.add_argument(
        "--format",
        help="Output format",
        choices=SUPPORTED_FORMATS,
        default="webp",
    )

    parser.add_argument("--quality", type=int, help="Quality of the output file")

    args = parser.parse_args()
    paths = [Path(p) for p in args.paths]
    output_format = args.format.lower()
    if output_format == "jpg":
        output_format = "jpeg"

    quality = args.quality if args.quality else DEFAULT_QUALITIES[output_format]

    if not validate_paths(paths):
        sys.exit()

    for path in paths:
        if path.is_dir():
            convert_folder_content(
                folder_path=path, output_format=output_format, quality=quality
            )
        elif path.is_file():
            status = convert_file(
                file_path=path, output_format=output_format, quality=quality
            )
            print(f"STATUS: {status['status']}, FILE: {status['file']}")


if __name__ == "__main__":
    main()
